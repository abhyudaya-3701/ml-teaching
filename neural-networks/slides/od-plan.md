# Detailed ML Slide Flow: Object Detection Lecture

## ✨ Section 0: Setting the Stage

### Slide 0: Title Slide

* **Title**: "Seeing with Algorithms: Deep Dive into Object Detection"
* **Subtitle**: "From Classification to Localization and Detection Metrics"
* Speaker info, course name, date

### Slide 1: Agenda / Learning Outcomes

* Understand classification, localization, detection
* Understand precision, recall, AP, mAP, CA-mAP
* Build strong intuition with toy examples
* Learn to evaluate detectors thoroughly

---

## 🌟 Section 1: Classification vs Localization vs Detection

### Slide 2: Task Definitions

* **Classification**: What is present in the image?
* **Localization**: Where is the object in the image?
* **Detection** = Classification + Localization (for multiple objects)

### Slide 3: Examples

* Image 1: Single dog (classification)
* Image 2: Dog with bounding box (localization)
* Image 3: Dog, person, bike (detection)
* Use **TikZ** overlays to show each task progressively on same image

### Slide 4: Output Formats

* Classification: `label`
* Localization: `label, bbox`
* Detection: `[label, confidence, bbox] x N`
* Show table of output formats side-by-side

---

## 🔬 Section 2: Bounding Boxes & Coordinates

### Slide 5: What is a Bounding Box?

* Format: `(x_min, y_min, x_max, y_max)` or `(x_center, y_center, width, height)`
* **TikZ**: Draw image grid with bounding box visualization

### Slide 6: Ground Truth vs Prediction

* Show one image with GT box and 3 predicted boxes (good, shifted, wrong class)
* Introduce idea of matching

---

## ✨ Section 3: IoU (Intersection over Union)

### Slide 7: IoU Definition

$\text{IoU} = \frac{\text{Area of Overlap}}{\text{Area of Union}}$

* **TikZ**: Two overlapping boxes with color-coded intersection and union

### Slide 8: IoU Calculation (Hand Example)

* GT: (30, 30, 100, 100)
* Pred: (50, 50, 120, 120)
* Step-by-step area calculation

---

## 📊 Section 4: Precision and Recall

### Slide 9: Definitions

$$
\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}
$$

* Emphasize: Precision = quality, Recall = coverage

### Slide 10: Example Image with TP, FP, FN

* 2 GT boxes
* 3 predictions (2 match, 1 FP)
* Count TP, FP, FN
* Compute precision and recall

---

## 📊 Section 5: Ranking and PR Curve

### Slide 11: Ranked Predictions Table

* Show detection table sorted by confidence:

```
Conf | Class | Box | TP/FP
0.95 | Dog   | ... | TP
0.88 | Bike  | ... | FP
0.80 | Dog   | ... | TP
0.70 | Person| ... | TP
0.40 | Cat   | ... | FP
```

* Compute cumulative TP, FP

### Slide 12: Precision-Recall Table

* Create columns:

  * Threshold, TP, FP, Precision, Recall
  * Build 6 points

### Slide 13: Draw PR Curve (TikZ)

* Plot points
* Show how AP = area under PR curve

---

## 🪙 Section 6: Average Precision (AP)

### Slide 14: AP = Area under PR curve

* Numerical integration or 11-pt interpolation
* Calculate AP for Dog = 0.85

### Slide 15: Class-wise AP

* Dog = 0.85
* Person = 0.71
* Bike = 0.40
* Table + plot

---

## 📊 Section 7: Mean AP and Class-Agnostic mAP

### Slide 16: mAP

$\text{mAP} = \frac{1}{C} \sum \text{AP}_c$

* Example with 3 classes: (0.85 + 0.71 + 0.40)/3 = **0.653**

### Slide 17: Class-Agnostic mAP

* Ignore class when matching GT and pred
* Recalculate:

  * Match only by IoU
  * CA-AP = 0.78 (say)
* Highlight when it is useful: weak supervision, generic object detection

---

## ⚠️ Section 8: Negative Images and FPs

### Slide 18: Negative Set Example

* Image has no object
* Detector predicts 4 boxes
* All are FPs
* AP undefined (no GT)

### Slide 19: FP Rate

* Table:

```
Image | #Pred | #FP
img3  | 4     | 4
```

* Metric: False Positive Rate = FP / total predictions

---

## 🔍 Section 9: Detection Errors

### Slide 20: Localization Errors

* GT box vs predicted box (IoU < 0.5)
* Show visually using **TikZ**

### Slide 21: Classification Errors

* Box overlaps well but wrong class
* Show: GT = dog, pred = person

### Slide 22: Duplicate Detection

* 2 predictions on same object
* Show suppression by Non-Maximum Suppression (NMS)

---

## 📊 Section 10: Strict Evaluation (COCO Style)

### Slide 23: AP\@50, AP\@75, AP@\[.5:.95]

* Explain:

  * AP\@50 = IoU ≥ 0.5
  * AP\@75 = stricter
  * AP@\[.5:.95] = average over IoU thresholds
* Table example:

```
Metric       | Value
---------------------
mAP@50       | 0.71
mAP@[.5:.95] | 0.42
```

---

## 🎓 Section 11: Interactive Quiz

### Slide 24: Compute Precision/Recall

* Image with 3 GT boxes, 5 predictions
* Ask students to:

  * Match boxes (use IoU)
  * Count TP, FP, FN
  * Compute Precision and Recall

### Slide 25: AP and mAP from scratch

* Given PR table
* Ask to compute AP
* Then average for mAP

---

## 📈 Section 12: Tools and Demos

### Slide 26: YOLOv8 Demo

* Show image upload + prediction
* Visualize detection boxes with confidence scores

### Slide 27: HuggingFace Spaces / Roboflow

* Show example of live model
* Try empty image (negative set)

---

## 🔗 Section 13: Wrap-up & Takeaways

### Slide 28: Summary Table

| Concept   | Meaning          | Visual                     |
| --------- | ---------------- | -------------------------- |
| IoU       | Matching quality | Box overlap                |
| Precision | Quality          | PR Curve                   |
| Recall    | Coverage         | PR Curve                   |
| AP        | Area under curve | PR                         |
| mAP       | Avg over classes | Table                      |
| CA-mAP    | Ignore class     | Useful in weak supervision |
| FP Rate   | Background error | Negative images            |

### Slide 29: Closing Slide

* "Detection is not just about finding objects, but finding them right."
* Include reference links, next topic preview

---

Let me know if you'd like the LaTeX Beamer + TikZ implementation of this plan next.
