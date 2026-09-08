# PyTorch Training Playbook

## Overview
Panduan training PyTorch dari nol sampai production: setup, training loop, debugging, optimization, dan deployment.

---

## ️ Project Structure

```
project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── dataset.py
├── models/
│   ├── __init__.py
│   └── model.py
├── training/
│   ├── train.py
│   ├── evaluate.py
│   └── utils.py
├── configs/
│   └── config.yaml
├── notebooks/
├── tests/
├── requirements.txt
└── README.md
```python

---

## Quick Start Template

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

# 1. Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Model
model = MyModel().to(device)

# 3. Loss & Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)

# 4. Scheduler
scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

# 5. Training Loop
for epoch in range(num_epochs):
    model.train()
    for batch in train_loader:
        inputs, targets = batch
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
    
    scheduler.step()
    
    # Evaluate
    val_loss, val_acc = evaluate(model, val_loader, criterion)
    print(f"Epoch {epoch+1}: val_loss={val_loss:.4f}, val_acc={val_acc:.4f}")
    
    # Save checkpoint
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_loss': val_loss,
    }, f'checkpoints/epoch_{epoch}.pt')
```python

---

## Data Pipeline

### Custom Dataset
```python
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = self.data[idx]
        label = self.labels[idx]
        
        if self.transform:
            sample = self.transform(sample)
        
        return sample, label
```

### DataLoader Best Practices
```python
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,        # CPU cores
    pin_memory=True,      # Faster GPU transfer
    drop_last=True,       # Consistent batch size
    persistent_workers=True  # Keep workers alive
)
```python

---

## Common Patterns

### Mixed Precision Training (FP16)
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in train_loader:
    optimizer.zero_grad()
    
    with autocast():
        outputs = model(inputs)
        loss = criterion(outputs, targets)
    
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
```

### Gradient Accumulation (Large Batches)
```python
accumulation_steps = 4

for i, batch in enumerate(train_loader):
    loss = criterion(model(inputs), targets) / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```python

### Early Stopping
```python
class EarlyStopping:
    def __init__(self, patience=5, min_delta=0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
    
    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                return True  # Stop training
        else:
            self.best_loss = val_loss
            self.counter = 0
        return False
```python

---

## Debugging

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Loss = NaN | Learning rate too high | Lower LR, check gradients |
| Loss not decreasing | Model not learning | Check data, increase model capacity |
| GPU OOM | Batch too large | Reduce batch size, use gradient accumulation |
| Slow training | No pin_memory, few workers | Increase workers, enable pin_memory |

### Gradient Checking
```python
# Check for NaN gradients
for name, param in model.named_parameters():
    if param.grad is not None:
        if torch.isnan(param.grad).any():
            print(f"NaN gradient in {name}")
```python

---

## Performance Optimization

### Memory Efficient
```python
# Delete unused variables
del outputs, loss
torch.cuda.empty_cache()

# Use gradient checkpointing for large models
from torch.utils.checkpoint import checkpoint
output = checkpoint(model.layer, input)
```

### Speed Up Training
```python
# Use torch.compile (PyTorch 2.0+)
model = torch.compile(model)

# Use DataLoader with prefetching
train_loader = DataLoader(..., prefetch_factor=2)
```

---

## Training Checklist

### Before Training
- [ ] Data properly split (train/val/test)
- [ ] Data loaders configured
- [ ] Model on correct device
- [ ] Loss function appropriate for task
- [ ] Learning rate reasonable (start with 1e-4)

### During Training
- [ ] Monitor training & validation loss
- [ ] Check for overfitting
- [ ] Save checkpoints regularly
- [ ] Log metrics (loss, accuracy, LR)

### After Training
- [ ] Evaluate on test set
- [ ] Save final model
- [ ] Document hyperparameters
- [ ] Version control model

---

## References
- https://pytorch.org/tutorials/
- https://pytorch.org/docs/stable/notes/cuda.html
- https://arxiv.org/abs/1706.03762 (Attention Is All You Need)

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
