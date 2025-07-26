#!/usr/bin/env python3
"""
Enhance notebook metadata with comprehensive and specific tags.

This script analyzes notebook content and metadata to add more comprehensive tags
based on actual content, imports, and ML concepts used.
"""

import json
import shutil
import re
from pathlib import Path
from collections import defaultdict

def extract_tags_from_content(notebook_data, filename):
    """Extract comprehensive tags from notebook content and filename."""
    tags = set()
    
    # Get all source code from cells
    all_source = ""
    for cell in notebook_data.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            all_source += source + "\n"
    
    # Filename-based tags (enhanced)
    stem = filename.lower().replace('-', ' ').replace('_', ' ')
    
    # Core ML Topics
    if any(word in stem for word in ['linear', 'regression']) and 'logistic' not in stem:
        tags.update(['linear-regression', 'supervised-learning', 'regression', 'optimization'])
    if any(word in stem for word in ['logistic', 'classification']):
        tags.update(['logistic-regression', 'classification', 'supervised-learning', 'optimization'])
    if any(word in stem for word in ['svm', 'support', 'vector']):
        tags.update(['svm', 'support-vector-machines', 'classification', 'supervised-learning', 'kernel-methods'])
    if any(word in stem for word in ['decision', 'tree']):
        tags.update(['decision-trees', 'supervised-learning', 'classification', 'regression', 'interpretability'])
    if any(word in stem for word in ['knn', 'k-nearest', 'neighbors']):
        tags.update(['knn', 'k-nearest-neighbors', 'supervised-learning', 'classification', 'regression'])
    if any(word in stem for word in ['naive', 'bayes']):
        tags.update(['naive-bayes', 'classification', 'supervised-learning', 'probabilistic'])
    if any(word in stem for word in ['ensemble', 'random', 'forest', 'boosting', 'adaboost']):
        tags.update(['ensemble-methods', 'supervised-learning', 'boosting', 'bagging'])
    if any(word in stem for word in ['neural', 'network', 'mlp', 'perceptron']):
        tags.update(['neural-networks', 'deep-learning', 'supervised-learning', 'optimization'])
    if any(word in stem for word in ['cnn', 'conv', 'lenet', 'vgg']):
        tags.update(['cnn', 'convolutional-neural-networks', 'deep-learning', 'computer-vision'])
    if any(word in stem for word in ['rnn', 'lstm', 'gru']):
        tags.update(['rnn', 'recurrent-neural-networks', 'deep-learning', 'sequence-modeling'])
    
    # Unsupervised Learning
    if any(word in stem for word in ['pca', 'principal', 'component']):
        tags.update(['pca', 'dimensionality-reduction', 'unsupervised-learning', 'feature-extraction'])
    if any(word in stem for word in ['kmeans', 'cluster', 'clustering']):
        tags.update(['clustering', 'k-means', 'unsupervised-learning'])
    if any(word in stem for word in ['autoencoder', 'ae']):
        tags.update(['autoencoders', 'unsupervised-learning', 'deep-learning', 'representation-learning'])
    
    # Optimization & Training
    if any(word in stem for word in ['gradient', 'descent']):
        tags.update(['gradient-descent', 'optimization', 'training', 'algorithms'])
    if any(word in stem for word in ['sgd', 'stochastic']):
        tags.update(['sgd', 'stochastic-gradient-descent', 'optimization'])
    if any(word in stem for word in ['adam', 'optimizer']):
        tags.update(['optimization', 'adaptive-methods', 'training'])
    if any(word in stem for word in ['backprop', 'backpropagation']):
        tags.update(['backpropagation', 'neural-networks', 'training', 'optimization'])
    
    # Model Evaluation & Selection
    if any(word in stem for word in ['bias', 'variance']):
        tags.update(['bias-variance-tradeoff', 'model-evaluation', 'generalization', 'overfitting'])
    if any(word in stem for word in ['cross', 'validation', 'cv']):
        tags.update(['cross-validation', 'model-evaluation', 'hyperparameter-tuning'])
    if any(word in stem for word in ['confusion', 'matrix']):
        tags.update(['confusion-matrix', 'classification-metrics', 'model-evaluation'])
    if any(word in stem for word in ['roc', 'auc', 'pr', 'curve']):
        tags.update(['roc-curve', 'auc', 'classification-metrics', 'model-evaluation'])
    if any(word in stem for word in ['hyperparameter', 'tuning', 'grid', 'search']):
        tags.update(['hyperparameter-tuning', 'model-selection', 'optimization'])
    
    # Regularization
    if any(word in stem for word in ['ridge', 'l2']):
        tags.update(['ridge-regression', 'l2-regularization', 'regularization', 'linear-regression'])
    if any(word in stem for word in ['lasso', 'l1']):
        tags.update(['lasso-regression', 'l1-regularization', 'regularization', 'linear-regression', 'feature-selection'])
    if any(word in stem for word in ['elastic', 'net']):
        tags.update(['elastic-net', 'regularization', 'linear-regression'])
    if any(word in stem for word in ['dropout', 'batch', 'norm']):
        tags.update(['regularization', 'neural-networks', 'deep-learning'])
    
    # Reinforcement Learning
    if any(word in stem for word in ['rl', 'reinforcement', 'q-learning', 'policy']):
        tags.update(['reinforcement-learning', 'q-learning', 'markov-decision-process'])
    if any(word in stem for word in ['gym', 'environment']):
        tags.update(['reinforcement-learning', 'openai-gym', 'simulation'])
    
    # Advanced Topics
    if any(word in stem for word in ['gan', 'generative']):
        tags.update(['gans', 'generative-adversarial-networks', 'deep-learning', 'generative-models'])
    if any(word in stem for word in ['transformer', 'attention']):
        tags.update(['transformers', 'attention-mechanism', 'deep-learning', 'nlp'])
    if any(word in stem for word in ['bert', 'gpt', 'llm']):
        tags.update(['large-language-models', 'nlp', 'transformers', 'deep-learning'])
    if any(word in stem for word in ['federated', 'distributed']):
        tags.update(['federated-learning', 'distributed-computing', 'privacy'])
    
    # Data & Preprocessing
    if any(word in stem for word in ['data', 'preprocessing', 'cleaning']):
        tags.update(['data-preprocessing', 'data-cleaning', 'feature-engineering'])
    if any(word in stem for word in ['feature', 'selection', 'extraction']):
        tags.update(['feature-selection', 'feature-engineering', 'dimensionality-reduction'])
    if any(word in stem for word in ['normalization', 'scaling', 'standardization']):
        tags.update(['data-preprocessing', 'normalization', 'feature-scaling'])
    
    # Applications
    if any(word in stem for word in ['mnist', 'digit', 'image']):
        tags.update(['mnist', 'computer-vision', 'image-classification'])
    if any(word in stem for word in ['nlp', 'text', 'language']):
        tags.update(['nlp', 'text-processing', 'natural-language-processing'])
    if any(word in stem for word in ['time', 'series', 'temporal']):
        tags.update(['time-series', 'temporal-data', 'forecasting'])
    if any(word in stem for word in ['recommendation', 'recommender']):
        tags.update(['recommendation-systems', 'collaborative-filtering', 'matrix-factorization'])
    if any(word in stem for word in ['object', 'detection', 'segmentation']):
        tags.update(['object-detection', 'computer-vision', 'image-segmentation'])
    
    # Technical Implementation
    if any(word in stem for word in ['numpy', 'pandas', 'sklearn']):
        tags.update(['python-libraries', 'scikit-learn', 'data-science'])
    if any(word in stem for word in ['torch', 'pytorch', 'tensorflow']):
        tags.update(['pytorch', 'deep-learning-frameworks', 'neural-networks'])
    if any(word in stem for word in ['gpu', 'cuda', 'acceleration']):
        tags.update(['gpu-computing', 'cuda', 'performance-optimization'])
    if any(word in stem for word in ['visualization', 'plot', 'chart']):
        tags.update(['data-visualization', 'matplotlib', 'plotting'])
    if any(word in stem for word in ['math', 'mathematics', 'linear', 'algebra']):
        tags.update(['mathematics', 'linear-algebra', 'calculus', 'statistics'])
    
    # Content-based analysis
    all_source_lower = all_source.lower()
    
    # Import-based tags
    if 'import torch' in all_source or 'from torch' in all_source:
        tags.update(['pytorch', 'deep-learning-frameworks'])
    if 'import tensorflow' in all_source or 'from tensorflow' in all_source:
        tags.update(['tensorflow', 'deep-learning-frameworks'])
    if 'import sklearn' in all_source or 'from sklearn' in all_source:
        tags.update(['scikit-learn', 'python-libraries'])
    if 'import numpy' in all_source or 'from numpy' in all_source:
        tags.update(['numpy', 'python-libraries'])
    if 'import pandas' in all_source or 'from pandas' in all_source:
        tags.update(['pandas', 'data-manipulation'])
    if 'import matplotlib' in all_source or 'import seaborn' in all_source:
        tags.update(['data-visualization', 'matplotlib', 'plotting'])
    if 'import gym' in all_source or 'from gym' in all_source:
        tags.update(['openai-gym', 'reinforcement-learning'])
    
    # Function/method-based tags
    if any(method in all_source_lower for method in ['fit(', 'predict(', 'transform(']):
        tags.add('scikit-learn')
    if any(method in all_source_lower for method in ['forward(', 'backward(', '.cuda()']):
        tags.update(['pytorch', 'deep-learning'])
    if any(method in all_source_lower for method in ['conv1d', 'conv2d', 'maxpool']):
        tags.update(['cnn', 'convolutional-neural-networks'])
    if any(method in all_source_lower for method in ['lstm', 'gru', 'rnn']):
        tags.update(['rnn', 'recurrent-neural-networks'])
    if any(method in all_source_lower for method in ['attention', 'transformer']):
        tags.update(['attention-mechanism', 'transformers'])
    
    # Algorithm-specific patterns
    if any(pattern in all_source_lower for pattern in ['gradientdescentoptimizer', 'adam', 'sgd']):
        tags.update(['optimization', 'gradient-descent'])
    if any(pattern in all_source_lower for pattern in ['cross_val_score', 'kfold', 'stratifiedkfold']):
        tags.update(['cross-validation', 'model-evaluation'])
    if any(pattern in all_source_lower for pattern in ['gridsearchcv', 'randomizedsearchcv']):
        tags.update(['hyperparameter-tuning', 'model-selection'])
    
    # Mathematical concepts
    if any(concept in all_source_lower for concept in ['eigenvalue', 'eigenvector', 'svd']):
        tags.update(['linear-algebra', 'mathematics'])
    if any(concept in all_source_lower for concept in ['probability', 'bayes', 'likelihood']):
        tags.update(['probability-theory', 'statistics', 'bayesian-methods'])
    if any(concept in all_source_lower for concept in ['derivative', 'gradient', 'jacobian']):
        tags.update(['calculus', 'optimization', 'mathematics'])
    
    # Always add these general tags
    tags.update(['machine-learning', 'tutorial', 'interactive'])
    
    # Domain-specific tags based on combinations
    if {'neural-networks', 'computer-vision'}.issubset(tags):
        tags.add('deep-computer-vision')
    if {'neural-networks', 'nlp'}.issubset(tags):
        tags.add('deep-nlp')
    if {'classification', 'supervised-learning'}.issubset(tags):
        tags.add('classification-algorithms')
    if {'regression', 'supervised-learning'}.issubset(tags):
        tags.add('regression-algorithms')
    
    return sorted(list(tags))

def get_current_tags(notebook_data):
    """Extract current tags from notebook metadata."""
    if not notebook_data.get('cells'):
        return []
    
    first_cell = notebook_data['cells'][0]
    if first_cell.get('cell_type') != 'raw':
        return []
    
    source = ''.join(first_cell.get('source', []))
    
    # Parse YAML to extract tags
    import re
    tags_match = re.search(r'tags:\s*\[(.*?)\]', source, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(1)
        # Extract quoted strings
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    
    return []

def update_notebook_tags(notebook_path, dry_run=False):
    """Update notebook with enhanced tags."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)
    
    # Get current and new tags
    current_tags = get_current_tags(notebook_data)
    new_tags = extract_tags_from_content(notebook_data, notebook_path.stem)
    
    # Combine and deduplicate
    all_tags = sorted(list(set(current_tags + new_tags)))
    
    if set(current_tags) == set(all_tags):
        return False, f"Tags already comprehensive ({len(current_tags)} tags)"
    
    print(f"Enhancing tags for {notebook_path.name}:")
    print(f"  Current tags ({len(current_tags)}): {current_tags[:3]}{'...' if len(current_tags) > 3 else ''}")
    print(f"  Enhanced tags ({len(all_tags)}): {all_tags[:5]}{'...' if len(all_tags) > 5 else ''}")
    print(f"  Added {len(all_tags) - len(current_tags)} new tags")
    
    if dry_run:
        print("  [DRY RUN - no changes made]")
        return True, "Would enhance tags"
    
    # Update the raw cell with new tags
    if notebook_data.get('cells') and notebook_data['cells'][0].get('cell_type') == 'raw':
        source = ''.join(notebook_data['cells'][0].get('source', []))
        
        # Format new tags
        tags_yaml = '[' + ', '.join(f'"{tag}"' for tag in all_tags) + ']'
        
        # Replace tags in YAML
        new_source = re.sub(r'tags:\s*\[.*?\]', f'tags: {tags_yaml}', source, flags=re.DOTALL)
        
        # Update the cell
        notebook_data['cells'][0]['source'] = [new_source]
        
        # Backup and save
        backup_path = notebook_path.with_suffix('.ipynb.backup-tags')
        shutil.copy2(notebook_path, backup_path)
        
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Enhanced tags and created backup: {backup_path.name}")
        return True, "Enhanced tags"
    
    return False, "No raw metadata cell found"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enhance notebook metadata with comprehensive tags")
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    parser.add_argument('--limit', type=int, help='Limit number of notebooks to process')
    args = parser.parse_args()
    
    notebooks = list(Path('notebooks').glob('**/*.ipynb'))
    if args.limit:
        notebooks = notebooks[:args.limit]
    
    print(f"Found {len(notebooks)} notebooks to enhance:")
    
    enhanced_count = 0
    tag_stats = defaultdict(int)
    
    for notebook in sorted(notebooks):
        try:
            enhanced, reason = update_notebook_tags(notebook, dry_run=args.dry_run)
            if enhanced:
                enhanced_count += 1
                # Collect tag statistics
                if not args.dry_run:
                    new_tags = extract_tags_from_content(
                        json.load(open(notebook, 'r')), 
                        notebook.stem
                    )
                    for tag in new_tags:
                        tag_stats[tag] += 1
            else:
                print(f"Skipped {notebook.name}: {reason}")
            print()
        except Exception as e:
            print(f"  ✗ Error processing {notebook.name}: {e}")
            print()
    
    print(f"Summary: {enhanced_count} notebooks {'would be ' if args.dry_run else ''}enhanced")
    
    if not args.dry_run and tag_stats:
        print(f"\nMost common tags:")
        for tag, count in sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {tag}: {count} notebooks")

if __name__ == '__main__':
    main()