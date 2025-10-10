"""
Generate diagrams for PR and ROC curve slides using latexify
"""
import sys
import os
sys.path.append('/Users/nipun/git/ml-teaching/notebooks')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.size': 8,
    'axes.labelsize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
})

# Output directory
output_dir = "/Users/nipun/git/ml-teaching/supervised/slides/"

# Use latexify for all plots - 1:1 aspect ratio for Beamer
# Using 4 inches for square plots (fits well in Beamer columns)
SQUARE_SIZE = 4.0

def save_plot(filename):
    """Save plot with tight layout"""
    plt.tight_layout()
    plt.savefig(f'{output_dir}{filename}', bbox_inches='tight', dpi=300)
    print(f"Created {filename}")
    plt.close()

# 1. Confusion Matrix Diagram
def create_confusion_matrix():
    fig, ax = plt.subplots(1, 1, figsize=(SQUARE_SIZE, SQUARE_SIZE))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Draw boxes with LaTeX text
    from matplotlib.patches import FancyBboxPatch

    # TP box (top-left)
    tp_box = FancyBboxPatch((1, 5.5), 3.5, 3.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='green', facecolor='lightgreen',
                            linewidth=2, alpha=0.7)
    ax.add_patch(tp_box)
    ax.text(2.75, 7.25, r'\textbf{TP}' + '\n' + r'True' + '\n' + r'Positive',
           ha='center', va='center', fontsize=14)

    # FN box (top-right)
    fn_box = FancyBboxPatch((5.5, 5.5), 3.5, 3.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='red', facecolor='lightcoral',
                            linewidth=2, alpha=0.7)
    ax.add_patch(fn_box)
    ax.text(7.25, 7.25, r'\textbf{FN}' + '\n' + r'False' + '\n' + r'Negative',
           ha='center', va='center', fontsize=14)

    # FP box (bottom-left)
    fp_box = FancyBboxPatch((1, 1), 3.5, 3.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='orange', facecolor='lightyellow',
                            linewidth=2, alpha=0.7)
    ax.add_patch(fp_box)
    ax.text(2.75, 2.75, r'\textbf{FP}' + '\n' + r'False' + '\n' + r'Positive',
           ha='center', va='center', fontsize=14)

    # TN box (bottom-right)
    tn_box = FancyBboxPatch((5.5, 1), 3.5, 3.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='blue', facecolor='lightblue',
                            linewidth=2, alpha=0.7)
    ax.add_patch(tn_box)
    ax.text(7.25, 2.75, r'\textbf{TN}' + '\n' + r'True' + '\n' + r'Negative',
           ha='center', va='center', fontsize=14)

    # Labels
    ax.text(5, 9.5, r'\textbf{Predicted}', ha='center', va='center', fontsize=12)
    ax.text(2.75, 9.2, r'Positive', ha='center', va='center', fontsize=10)
    ax.text(7.25, 9.2, r'Negative', ha='center', va='center', fontsize=10)

    ax.text(0.3, 7.25, r'Positive', ha='center', va='center',
           fontsize=10, rotation=90)
    ax.text(0.3, 2.75, r'Negative', ha='center', va='center',
           fontsize=10, rotation=90)
    ax.text(-0.2, 5, r'\textbf{Actual}', ha='center', va='center',
           fontsize=12, rotation=90)

    save_plot('confusion-matrix-diagram.pdf')

# 2. PR Curve with annotations
def create_pr_curve():
    fig, ax = plt.subplots(1, 1, figsize=(SQUARE_SIZE, SQUARE_SIZE))

    # Simulate a PR curve
    recall = np.array([0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0])
    precision = np.array([1.0, 0.95, 0.92, 0.88, 0.82, 0.75, 0.68, 0.62, 0.55, 0.52, 0.48])

    # Plot curve
    ax.plot(recall, precision, 'b-', linewidth=2.5, label='Model PR Curve')
    ax.fill_between(recall, 0, precision, alpha=0.2, color='blue')

    # Baseline
    baseline = 0.48
    ax.axhline(y=baseline, color='red', linestyle='--', linewidth=2,
              label=f'Random (AP={baseline:.2f})')

    # Perfect classifier point
    ax.plot([1], [1], 'g*', markersize=15, label='Perfect')

    # Annotate key points with arrows
    # High precision point
    ax.plot([0.2], [0.95], 'ro', markersize=10)
    ax.annotate(r'High Prec.' + '\n' + r'Low Recall',
               xy=(0.2, 0.95), xytext=(0.35, 0.85),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='red'),
               fontsize=8, ha='center')

    # Balanced point
    ax.plot([0.7], [0.75], 'mo', markersize=10)
    ax.annotate(r'Balanced',
               xy=(0.7, 0.75), xytext=(0.5, 0.6),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'),
               fontsize=8, ha='center')

    # High recall point
    ax.plot([0.95], [0.52], 'co', markersize=10)
    ax.annotate(r'High Recall' + '\n' + r'Low Prec.',
               xy=(0.95, 0.52), xytext=(0.7, 0.3),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='cyan'),
               fontsize=8, ha='center')

    ax.set_xlabel(r'Recall', fontsize=10)
    ax.set_ylabel(r'Precision', fontsize=10)
    ax.set_xlim([0, 1.05])
    ax.set_ylim([0, 1.05])
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.legend(loc='upper right', fontsize=7, framealpha=0.9)
    ax.set_aspect('equal')
    pass  # format_axes(ax)

    save_plot('pr-curve-diagram.pdf')

# 3. ROC Curve with annotations
def create_roc_curve():
    fig, ax = plt.subplots(1, 1, figsize=(SQUARE_SIZE, SQUARE_SIZE))

    # Simulate a ROC curve
    fpr = np.array([0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 0.85, 1.0])
    tpr = np.array([0, 0.4, 0.6, 0.72, 0.8, 0.87, 0.92, 0.95, 0.98, 0.99, 1.0])

    # Plot ROC curve
    ax.plot(fpr, tpr, 'b-', linewidth=2.5, label='Model ROC')
    ax.fill_between(fpr, 0, tpr, alpha=0.2, color='blue', label='AUC')

    # Diagonal (random classifier)
    ax.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Random (AUC=0.5)')

    # Perfect classifier
    ax.plot([0, 0, 1], [0, 1, 1], 'g--', linewidth=2, alpha=0.5, label='Perfect (AUC=1.0)')

    # Annotate key points
    # Top-left corner (ideal)
    ax.plot([0], [1], 'g*', markersize=15)
    ax.annotate(r'Ideal' + '\n' + r'(TPR=1, FPR=0)',
               xy=(0, 1), xytext=(0.25, 0.9),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='green'),
               fontsize=8, ha='center')

    # Good operating point
    ax.plot([0.15], [0.72], 'mo', markersize=10)
    ax.annotate(r'Good Trade-off',
               xy=(0.15, 0.72), xytext=(0.4, 0.55),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'),
               fontsize=8, ha='center')

    ax.set_xlabel(r'False Positive Rate (FPR)', fontsize=10)
    ax.set_ylabel(r'True Positive Rate (TPR)', fontsize=10)
    ax.set_xlim([0, 1.05])
    ax.set_ylim([0, 1.05])
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.legend(loc='lower right', fontsize=7, framealpha=0.9)
    ax.set_aspect('equal')
    pass  # format_axes(ax)

    save_plot('roc-curve-diagram.pdf')

# 4. AUC visualization - side by side
def create_auc_diagram():
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(SQUARE_SIZE*2.2, SQUARE_SIZE))

    # AUC-PR
    recall = np.linspace(0, 1, 50)
    precision = 1 - 0.5 * recall + 0.1 * np.sin(recall * 5)
    precision = np.clip(precision, 0.4, 1.0)

    ax1.plot(recall, precision, 'b-', linewidth=2.5, label='Model PR')
    ax1.fill_between(recall, 0, precision, alpha=0.3, color='blue', label='AP')
    ax1.axhline(y=0.48, color='red', linestyle='--', linewidth=1.5, label='Random')
    ax1.set_xlabel(r'Recall', fontsize=10)
    ax1.set_ylabel(r'Precision', fontsize=10)
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.05])
    ax1.grid(True, alpha=0.3, linewidth=0.5)
    ax1.legend(loc='best', fontsize=7)
    ax1.text(0.5, 0.5, r'AUC-PR $\approx$ 0.82', fontsize=10,
            ha='center', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    pass  # format_axes(ax1)

    # AUC-ROC
    fpr = np.linspace(0, 1, 50)
    tpr = np.sqrt(fpr) * 0.8 + 0.2 * fpr
    tpr = np.clip(tpr, 0, 1.0)

    ax2.plot(fpr, tpr, 'b-', linewidth=2.5, label='Model ROC')
    ax2.fill_between(fpr, 0, tpr, alpha=0.3, color='blue', label='AUC-ROC')
    ax2.plot([0, 1], [0, 1], 'r--', linewidth=1.5, label='Random')
    ax2.set_xlabel(r'False Positive Rate', fontsize=10)
    ax2.set_ylabel(r'True Positive Rate', fontsize=10)
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.05])
    ax2.grid(True, alpha=0.3, linewidth=0.5)
    ax2.legend(loc='lower right', fontsize=7)
    ax2.set_aspect('equal')
    ax2.text(0.6, 0.3, r'AUC-ROC $\approx$ 0.85', fontsize=10,
            ha='center', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    pass  # format_axes(ax2)

    save_plot('auc-diagram.pdf')

# 5. Threshold effect diagram
def create_threshold_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(SQUARE_SIZE*1.4, SQUARE_SIZE*0.8))

    # Sample probabilities and true labels
    np.random.seed(42)
    n_samples = 40
    # Positive class (higher probabilities)
    pos_probs = np.random.beta(5, 2, n_samples//2)
    # Negative class (lower probabilities)
    neg_probs = np.random.beta(2, 5, n_samples//2)

    # Sort them
    pos_probs = np.sort(pos_probs)
    neg_probs = np.sort(neg_probs)

    # Plot distributions
    y_pos = np.ones(len(pos_probs)) * 1.2
    y_neg = np.zeros(len(neg_probs))

    ax.scatter(pos_probs, y_pos, c='red', s=50, alpha=0.6,
              label='Actual Positive', marker='^', edgecolors='black', linewidth=0.8)
    ax.scatter(neg_probs, y_neg, c='blue', s=50, alpha=0.6,
              label='Actual Negative', marker='o', edgecolors='black', linewidth=0.8)

    # Three different thresholds
    thresholds = [0.3, 0.5, 0.7]
    colors = ['green', 'orange', 'purple']

    for thresh, color in zip(thresholds, colors):
        ax.axvline(x=thresh, color=color, linestyle='--', linewidth=2,
                  alpha=0.7, label=rf'$\tau={thresh}$')

        # Count predictions
        tp = (pos_probs >= thresh).sum()
        fn = (pos_probs < thresh).sum()
        fp = (neg_probs >= thresh).sum()
        tn = (neg_probs < thresh).sum()

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    ax.set_xlabel(r'Predicted Probability', fontsize=10)
    ax.set_ylabel(r'True Class', fontsize=10)
    ax.set_yticks([0, 1.2])
    ax.set_yticklabels(['Negative', 'Positive'])
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.4, 1.6])
    ax.legend(loc='upper left', fontsize=7, framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='x', linewidth=0.5)
    pass  # format_axes(ax)

    save_plot('threshold-effect-diagram.pdf')

# 6. Model comparison diagram
def create_model_comparison():
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(SQUARE_SIZE*2.2, SQUARE_SIZE))

    # Three models
    models = ['Model A', 'Model B', 'Model C']
    colors = ['blue', 'green', 'red']

    # PR curves
    for i, (model, color) in enumerate(zip(models, colors)):
        recall = np.linspace(0, 1, 50)
        # Different curves for different models
        precision = 1 - 0.4 * recall + 0.1 * np.sin(recall * 5) - i * 0.1
        precision = np.clip(precision, 0.3, 1.0)
        ax1.plot(recall, precision, linewidth=2.5, label=model, color=color)

    ax1.axhline(y=0.5, color='gray', linestyle='--', linewidth=1.5, label='Baseline')
    ax1.set_xlabel(r'Recall', fontsize=10)
    ax1.set_ylabel(r'Precision', fontsize=10)
    ax1.legend(loc='best', fontsize=7)
    ax1.grid(True, alpha=0.3, linewidth=0.5)
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.05])
    pass  # format_axes(ax1)

    # ROC curves
    for i, (model, color) in enumerate(zip(models, colors)):
        fpr = np.linspace(0, 1, 50)
        tpr = fpr**0.5 * (1 - i * 0.15) + 0.1 * i
        tpr = np.clip(tpr, 0, 1.0)
        ax2.plot(fpr, tpr, linewidth=2.5, label=model, color=color)

    ax2.plot([0, 1], [0, 1], 'gray', linestyle='--', linewidth=1.5, label='Random')
    ax2.set_xlabel(r'False Positive Rate', fontsize=10)
    ax2.set_ylabel(r'True Positive Rate', fontsize=10)
    ax2.legend(loc='lower right', fontsize=7)
    ax2.grid(True, alpha=0.3, linewidth=0.5)
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.05])
    ax2.set_aspect('equal')
    pass  # format_axes(ax2)

    save_plot('model-comparison-diagram.pdf')

# Generate all diagrams
if __name__ == "__main__":
    print("Generating PR and ROC curve diagrams with latexify...")
    create_confusion_matrix()
    create_pr_curve()
    create_roc_curve()
    create_auc_diagram()
    create_threshold_diagram()
    create_model_comparison()
    print("\nAll diagrams generated successfully with LaTeX formatting!")
