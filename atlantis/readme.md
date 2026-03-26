# Atlantis

## Commands
```
# Fly
fly deploy
fly ssh console

# Local Conftest
tf plan -out=tfplan
tf show -json tfplan > plan.json
conftest test --policy ../../atlantis/policies plan.json 
```

