# LabelEditor（Dataset editor） [中文README](README.md)

[![wakatime](https://wakatime.com/badge/user/23381c4b-372b-46eb-b687-994db38af858/project/11416424-fb1a-4c94-be60-826ed08291f4.svg)](https://wakatime.com/badge/user/23381c4b-372b-46eb-b687-994db38af858/project/11416424-fb1a-4c94-be60-826ed08291f4)

#### Usage range:

this is a dataset tag editor that devlop for edit dataset of stable diffusion model embedding or dreambooth 

but it not means that it only can be used in the above application scenario

the editor is suitable for all datasets that meet the following conditions:

**the files are in the same folder, the images are in png format, and there is a txt file with the same name, which stores the tag corresponding to the png image, separated by `,`**

It is possible to use this batch editor if the above conditions are met

## Framework:

The front end uses Quasar to build, and the back end uses Python Flask to build the API server
 
In addition, the static file also exposed the compiled output directory of the Quasar project, which can be used as a static file server to provide browsing services for the web pages compiled by Quasar

`app.config.globalProperties.$DEBUG` in `public/src/boot/config.js` will determine whether the front-end request API uses the debug address (this is usually a makeshift measure when using quasar dev for front-end development), if False will use `/` as the root access API

## Development:

quasar: 2.x

python: >=3.7

### Front-end development

```bash
cd public && quasar dev
```

### Api server development

```bash
python main.py --host 107.0.0.1 --port 5000
```

## Function:

1. filtering images using tag (reverse filtering supported)
2. select the specified image for tag bulk add/remove operation
3. selected images can be reverse selected in the results of the Tag filter
4. support for adding custom tags
5. preview changes before saving (red for delete, green for add)

## Preview(the latest version was added i18n support, for chinese and english):
<img width="1897" alt="image" src="https://user-images.githubusercontent.com/84715902/218341196-687bdb28-1069-4ea5-a2d2-3a501aeb4c1b.png">
<div align="center">
  <img width="500" alt="屏幕截图_20221230_230055" src="https://user-images.githubusercontent.com/84715902/210116915-d25d3b22-8429-406c-9523-aa864d13fc97.png"/>
  <img width="500" alt="屏幕截图_20221230_230036" src="https://user-images.githubusercontent.com/84715902/210116918-04751e29-e440-4508-9bbf-aab601bfc7b9.png"/>
</div>
<img width="1108" alt="屏幕截图_20221230_230108" src="https://user-images.githubusercontent.com/84715902/210116925-fbb16bd0-cbb3-4c97-b4f1-2306aff52ef3.png">
<img width="1670" alt="屏幕截图_20221230_230128" src="https://user-images.githubusercontent.com/84715902/210116923-c3c5cfb5-4932-4ecb-b902-ad37efa1f720.png">
<img width="1873" alt="屏幕截图_20221230_230154" src="https://user-images.githubusercontent.com/84715902/210116919-70f38e6c-2616-490e-9ba9-ef4a57af1705.png">


