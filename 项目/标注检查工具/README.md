
可以用 pip 装，

```python 
# Install the package
pip install -U label-studio

# Launch it!
label-studio
```


也可以从 github clone 下来装。   

```python
# Clone repo
git clone https://github.com/heartexlabs/label-studio.git  

# Install dependencies
cd label-studio
pip install -e .

# Collect static files
python label_studio/manage.py collectstatic

# Launch
python label_studio/manage.py runserver
```

DJANGO_SETTINGS_MODULE 是 core.settings.label_studio    

