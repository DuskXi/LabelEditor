# LabelEditor（数据集Tag编辑器） [English](README_EN.md)

#### 适用范围：

  这是一个为了stable diffusion webui训练embedding或者dreambooth的数据集而生的一个数据集Tag批量化编辑器
  
  但是并不意味着仅限于上述应用场景
  
  编辑器适用于所有的以符合以下条件的数据集：
  
  **文件处于同一个文件夹，图像以png为扩展名，并且伴随一个同名的txt扩展名文件，其中储存了png图像所对应的tag，以`,`为分隔符分割**
  
  满足该条件就可以使用此批量化编辑器
  
## 架构:

前端使用Quasar搭建，后端使用Python Flask搭建API服务器

但是同时也使用静态文件暴露了Quasar项目的编译输出目录，可以作为静态文件服务器提供对Quasar编译后的网页的浏览服务

在`public/src/boot/config.js` 中的 `app.config.globalProperties.$DEBUG` 参数将会决定前端请求API时是否使用调试地址（这一般性作为使用quasar dev进行前端开发时的权宜之计），如果为False将会使用`/`作为根访问API
  
## 开发:

quasar: 2.x

python: >=3.7

### 前端开发

```bash
cd public && quasar dev
```

### 后端开发

```bash
python main.py --host 107.0.0.1 --port 5000
```

## 功能:

1. 对图像使用tag进行筛选（支持反向筛选）
2. 选择指定图像，进行tag的批量增/删操作
3. 选择的图像可以在Tag筛选器的结果中进行反选
4. 支持添加自定义Tag
5. 保存前预览更改（红为删，绿为增）

## 预览:
<div align="center">
  <img width="500" alt="屏幕截图_20221230_230055" src="https://user-images.githubusercontent.com/84715902/210116915-d25d3b22-8429-406c-9523-aa864d13fc97.png"/>
  <img width="500" alt="屏幕截图_20221230_230036" src="https://user-images.githubusercontent.com/84715902/210116918-04751e29-e440-4508-9bbf-aab601bfc7b9.png"/>
</div>
<img width="1108" alt="屏幕截图_20221230_230108" src="https://user-images.githubusercontent.com/84715902/210116925-fbb16bd0-cbb3-4c97-b4f1-2306aff52ef3.png">
<img width="1670" alt="屏幕截图_20221230_230128" src="https://user-images.githubusercontent.com/84715902/210116923-c3c5cfb5-4932-4ecb-b902-ad37efa1f720.png">
<img width="1873" alt="屏幕截图_20221230_230154" src="https://user-images.githubusercontent.com/84715902/210116919-70f38e6c-2616-490e-9ba9-ef4a57af1705.png">
<img width="1891" alt="image" src="https://user-images.githubusercontent.com/84715902/218340332-df3270a2-af77-4e88-b744-30034d79a3c9.png">

