<template>
    <q-page class="flex flex-center q-col-gutter-y-sm">
        <div class="row q-col-gutter-x-lg" style="width: 100%">
            <div class="col-7">
                <div class="row justify-center q-gutter-md">
                    <div class="text-h4">样本</div>
                    <q-scroll-area style="height: 90vh; width: 100vw;">
                        <div class="row justify-center q-gutter-md">
                            <q-intersection v-for="(enable, index) in visibleMask" :key="index" transition="scale" once class="example-item ">
                                <q-card class="q-ma-sm" v-if="enable"
                                        :style="'max-width: 256px; min-height: 256px;'+(dataSelected[index] && tagEditor?'transform: scale(1.1)':'')"
                                        v-on:mouseenter="$event.target.style.transform= 'scale(1.1)';"
                                        v-on:mouseleave="$event.target.style.transform= dataSelected[index] && tagEditor?'scale(1.1)':'scale(1)';"
                                        @click="()=>{if(tagEditor &&!keyBoardTable['Control'])dataSelected[index]=!dataSelected[index]}">
                                    <img :src="dataStore[index].imageDataUrl.length>0 ? dataStore[index].imageDataUrl : dataStore[index].imageResizeUrl" :alt="dataStore[index].imageName"
                                         style="width: 256px ;">
                                    <div class="maskT" v-if="dataSelected[index] && tagEditor" style="height: 256px">
                                        <div class="flex absolute-center">
                                            <q-icon name="check_circle" color="orange" style="transform: scale(3)"></q-icon>
                                        </div>
                                    </div>

                                    <q-card-section>
                                        <div class="text-h6"></div>
                                        <div class="text-subtitle2 q-gutter-x-sm">
                                            <q-badge v-for="(text, index) in dataStore[index].labels" :key="index" :color="this.labelChoose[text] ? 'orange':'secondary'"
                                                     @click="()=>{if (keyBoardTable['Control']) this.labelChoose[text] = !this.labelChoose[text];}"
                                                     :style="keyBoardTable['Control']?'cursor: pointer': 'auto'"
                                                     v-on:mouseenter="$event.target.style.transform= 'scale(1.1)';" v-on:mouseleave="$event.target.style.transform= 'scale(1)';">{{ text }}
                                            </q-badge>
                                        </div>
                                    </q-card-section>
                                    <div class="mask" v-if="dataSelected[index] && tagEditor"></div>
                                    <q-tooltip v-if="keyBoardTable['Alt']">
                                        {{ dataStore[index].filewords }}
                                    </q-tooltip>
                                </q-card>
                            </q-intersection>
                            <q-inner-loading :showing="imageLoading">
                                <q-spinner-gears size="50px" color="primary"/>
                            </q-inner-loading>
                        </div>
                    </q-scroll-area>
                </div>
            </div>
            <div class="col-5">
                <div class="row justify-center ">
                    <q-scroll-area style="height: 95vh; width: 100vw;">
                        <div class="col q-gutter-y-sm">
                            <div class="text-h4">Tags</div>
                            <q-expansion-item v-model="tagEditor" icon="edit" label="Tag 编辑" caption="TagEditor">
                                <q-card>
                                    <q-card-section class="q-gutter-y-sm q-gutter-x-sm" v-if="tagEditor">
                                        <q-btn color="positive" class="full-width" v-if="difference_data()[0]>0" @click="saveTag=true">保存({{ difference_data()[0] }})</q-btn>
                                        <q-dialog v-model="saveTag">
                                            <q-card :style="$q.screen.gt.sm? 'width: 1500px; max-width: 75vw;':'width: 95vw;'">
                                                <q-card-section>
                                                    <div class="text-h6">保存</div>
                                                </q-card-section>

                                                <q-card-section class="q-pt-none">
                                                    <div class="text-h5">一共 <span style="color: red">{{ difference_data()[0] }} </span> 项修改</div>
                                                    <div class="text-h6" v-for="(item, index) in difference_data()[1]" :key="index">
                                                        <span style="color: #00b0ff">[{{ index }}]: </span>
                                                        <span style="color: #b0bec5; font-size: 7px">[{{ /[0-9\-]+(?=(\x20|\.))/.exec(item[0].imageName)[0] }}]: </span>
                                                        <span v-html="item[0].color_filewords" style="font-size: 5px"></span>
                                                        <span style="color: orange">-></span>
                                                        <span v-html="item[1].color_filewords" style="font-size: 5px"></span>
                                                    </div>
                                                </q-card-section>

                                                <q-card-actions align="right">
                                                    <q-btn flat label="取消" color="black" v-close-popup/>
                                                    <q-btn flat label="保存" color="positive" @click="save" v-close-popup/>
                                                </q-card-actions>
                                            </q-card>
                                        </q-dialog>
                                        <div class="text-h5">已选中 <span style="color: orange">{{ dataSelected.filter((value) => value).length }} 条</span></div>
                                        <div class="text-h5">被选中的数据所拥有的Tags:</div>
                                        <div class="row q-gutter-x-sm">
                                            <q-toggle v-model="selectedShow" v-if="dataSelected.filter((value) => value).length > 0" label="只看选中的数据"/>
                                            <q-btn color="warning" @click="(()=>{selectedShow=false; dataSelected=dataSelected.map(()=>false);})"
                                                   :disable="dataSelected.filter((value) => value).length === 0">清除选择
                                            </q-btn>
                                            <q-btn color="secondary" @click="(()=>{selectedShow=false; dataSelected=dataSelected.map((value, index)=>visibleMask[index] ? !value:value);})"
                                                   :disable="dataSelected.filter((value) => value).length === dataSelected.length"
                                                   :label="dataSelected.filter((value) => value).length === 0 ?'取反(全选)': '取反'"/>
                                        </div>
                                        <div class="row">
                                            <q-expansion-item v-model="tagEditorFilter" icon="filter_alt" :label="tagEditorFilter?'收起过滤器':'展开过滤器'" caption="tagEditorFilter"
                                                              style="width: 100%">
                                                <q-card class="my-card q-gutter-y-none q-gutter-none" color="primary">
                                                    <q-checkbox v-for="(key, index) in keySortByValue(simpleLabelCount(dataSelected))" :key="index"
                                                                v-model="labelChoose[key]" color="teal"><span v-html="`${key} [${simpleLabelCount(dataSelected)[key]}]&nbsp;`"></span>
                                                        <q-btn icon="add" :dense="true"
                                                               @click="((event)=>{if(!labelOptions.includes(key))labelOptions.push(key); event.target.disabled=true; labelChoose[key]=!labelChoose[key];})"></q-btn>
                                                    </q-checkbox>
                                                </q-card>
                                            </q-expansion-item>
                                        </div>
                                        <q-select filled v-model="operateLabel" :options="labelOptions" label="请添加" hint="操作label">
                                            <template v-slot:append>
                                                <q-btn round dense flat icon="add" @click="addOptions=true"/>
                                                <q-dialog v-model="addOptions">
                                                    <q-card style="width: 45vw">
                                                        <q-card-section>
                                                            <div class="text-h6">添加自定义Tag</div>
                                                        </q-card-section>

                                                        <q-card-section class="q-pt-none">
                                                            <q-input v-model="newLabel" label="请输入新的Tag" filled clearable/>
                                                        </q-card-section>

                                                        <q-card-actions align="right">
                                                            <q-btn flat label="OK" color="primary" v-close-popup @click="addNewLabel"/>
                                                        </q-card-actions>
                                                    </q-card>
                                                </q-dialog>
                                            </template>
                                        </q-select>
                                        <q-btn color="positive" v-if="operateLabel!=='' && operateLabel!==null"
                                               :label="'向所有选择的'+ dataSelected.filter((value) => value).length +'条数据添加该标签'" @click="attachLabel(operateLabel)"/>
                                        <q-btn color="negative" v-if="simpleLabelCount(dataSelected).hasOwnProperty(operateLabel)" @click="detachLabel(operateLabel)"
                                               :label="'从所有选择的'+ dataSelected.filter((value) => value).length +'条数据移除改标签(可移除'+ simpleLabelCount(dataSelected)[operateLabel] +')'"/>
                                        <q-btn color="primary" v-if="movableLabelCount(operateLabel, 'forward') > 0" @click="moveLabel(operateLabel, 'forward')">
                                            <template v-slot:default>
                                                <q-icon name="arrow_back"/>
                                                {{ movableLabelCount(operateLabel, 'forward') }}
                                            </template>
                                        </q-btn>
                                        <q-btn color="primary" v-if="movableLabelCount(operateLabel, 'back') > 0" @click="moveLabel(operateLabel, 'back')">
                                            <template v-slot:default>
                                                {{ movableLabelCount(operateLabel, 'back') }}
                                                <q-icon name="arrow_forward"/>
                                            </template>
                                        </q-btn>
                                        <div class="row" v-if="movableLabelCount(operateLabel, 'back') + movableLabelCount(operateLabel, 'forward') > 0">
                                            <q-badge color="secondary"> Label relative position: {{ labelPosition }} % (0 to 100), index: {{ averageLabelPosition }}</q-badge>
                                            <q-slider v-model="labelPosition" :min="0" :max="100" @update:model-value="setLabelPosition(operateLabel, labelPosition / 100.0);"></q-slider>
                                        </div>
                                    </q-card-section>
                                </q-card>

                            </q-expansion-item>
                            <div class="row">
                                <q-input v-model="labelSearcher" hint="label搜索" filled autogrow :dense="false" style="width: 100%">
                                    <template v-slot:before>
                                        <q-icon name="search"/>
                                    </template>
                                    <template v-slot:after>
                                        <q-btn round dense flat icon="close" @click="labelSearcher=''"/>
                                    </template>
                                </q-input>
                            </div>
                            <div class="text-h6" v-if="chosenLabels.length > 0">负向过滤器:</div>
                            <div class="row" v-if="chosenLabels.length > 0">
                                <div class="q-gutter-none" v-for="(key, index) in chosenLabels" :key="index">
                                    <q-toggle left-label v-model="(labelFilterStrategyTable[key])">{{ key }}</q-toggle>
                                </div>
                            </div>
                            <div class="text-h6" v-if="visibleMask.filter(v => v).length > 0">过滤结果: {{ visibleMask.filter(v => v).length }}</div>
                            <div class="row q-gutter-md">
                                <div class="q-gutter-none">
                                    名称排序
                                    <q-toggle v-model="sortType" left-label></q-toggle>
                                    计数排序
                                </div>
                                <q-btn label="清空筛选器" @click="clearFilter" color="primary"></q-btn>
                                <q-toggle v-model="negativeShow" right-label>翻转结果</q-toggle>
                                <q-toggle v-model="enableBottomAdd" v-if="tagEditor" right-label>启用添加</q-toggle>
                                <div class="text-h6">过滤器逻辑运算方式</div>
                                <div class="q-gutter-none">
                                    And
                                    <q-toggle v-model="filterOperate" left-label></q-toggle>
                                    Or
                                </div>
                            </div>
                            <div class="row">
                                <q-card class="my-card" color="primary">
                                    <q-checkbox v-for="(key, index) in shownLabels" :key="index"
                                                v-model="labelChoose[key]" color="teal"><span v-html="`${highLight(key, labelSearcher)} [${labelClassify[key]}]&nbsp;`"></span>
                                        <q-btn icon="add" :dense="true" v-if="tagEditor && enableBottomAdd"
                                               @click="((event)=>{if(!labelOptions.includes(key))labelOptions.push(key); event.target.disabled=true; labelChoose[key]=!labelChoose[key];})"></q-btn>
                                    </q-checkbox>
                                </q-card>
                                <q-inner-loading
                                    :showing="tagLoading"
                                    label="Please wait..."
                                    label-class="text-teal"
                                    label-style="font-size: 1.1em"
                                />
                            </div>
                        </div>
                    </q-scroll-area>
                </div>
            </div>
        </div>
    </q-page>
</template>

<script>
import {defineComponent} from 'vue'

export default defineComponent({
    name: 'IndexPage',
    data: () => ({
        debug: false,
        base_url: '',
        files: [],
        archiveData: [],
        dataStore: [],
        visibleMask: [],
        dataSelected: [],
        selectedShow: false,
        labelClassify: {},
        labelItemMap: {},
        labelChoose: {},
        labelOptions: [],
        labelFilterStrategyTable: {},
        operateLabel: null,
        visibleLabels: {},
        labelSearcher: '',
        enableBottomAdd: false,
        sortType: true,
        negativeShow: false,
        filterOperate: false,
        keyImageViewer: new Date().getTime(),
        keyBoardTable: {},
        tagEditor: false,
        tagEditorFilter: true,
        addOptions: false,
        newLabel: '',
        saveTag: false,
        tagLoading: false,
        imageLoading: false,
        labelPosition: 0,
        labelPositionOperationProtect: false,
        averageLabelPosition: 0,
    }),
    computed: {
        shownLabels() {
            let sorted = (this.sortType ? this.labelsKeysSortByValue() : this.labelsKeysSortByKey());
            return sorted.filter((key) => this.visibleLabels[key]);
        },
        chosenLabels() {
            return this.shownLabels.filter((key) => this.labelChoose[key]);
        },
    },
    methods: {
        highLight(text, highlightText, color = 'red') {
            if (highlightText === '') return text
            let reg = new RegExp(highlightText, 'g')
            return text.replace(reg, `<span style="color: ${color}">${highlightText}</span>`)
        },
        getUrl(path) {
            return this.base_url + path
        },
        imageUrl(imageName) {
            return this.getUrl('/api/v1/image?image=' + imageName)
        },
        fileWordsUrl(fileName) {
            return this.getUrl('/api/v1/filewords?filename=' + fileName)
        },
        async loadFileWords(fileName) {
            const response = await fetch(this.fileWordsUrl(fileName))
            return await response.text()
        },
        async loadImage(imageName) {
            const response = await fetch(this.getUrl('/api/v1/imageBase64?image=' + imageName + '&width=256&height=256'))
            const data = await response.json()
            return data['imageBase64'];
        },
        async loadAllImage() {
            const response = await fetch(this.getUrl('/api/v1/imageBase64?all=ture&width=256&height=256'))
            const data = await response.json()
            return data['allImageBase64'];
        },
        async loadAllFileWords() {
            const response = await fetch(this.getUrl('/api/v1/filewords?all=ture'))
            const data = await response.json()
            return data['filewords'];
        },
        async save() {
            let [diff_number, diff] = this.difference_data();
            let savingData = {
                'data': diff,
            };
            let response = await fetch(this.getUrl('/api/v1/save'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(savingData)
            });
        },
        async getFiles() {
            this.imageLoading = true;
            const response = await fetch(this.getUrl("/api/v1/files"), {mode: 'cors'})
            const data = await response.json()
            this.dataStore = [];
            this.visibleMask = [];
            this.dataSelected = [];
            let allFilewords = await this.loadAllFileWords();
            let index = 0;
            data.files.forEach((file) => {
                this.dataStore.push({
                    imageName: file[0],
                    filewordsName: file[1],
                    filewords: allFilewords[file[0].replace(/\.png$/g, '')],
                    labels: this.getLabels(allFilewords[file[0].replace(/\.png$/g, '')]),
                    imageDataUrl: '',
                    imageResizeUrl: this.imageUrl(file[0]) + '&width=256&height=256',
                })
                this.visibleMask.push(true);
                this.dataSelected.push(false);
                index++;
            })
            let allImage = await this.loadAllImage();
            this.dataStore.forEach((file) => {
                file.imageDataUrl = allImage[file.imageName.replace(/\.png$/g, '')];
            })
            this.imageLoading = false;
            this.keyImageViewer = new Date().getTime();
            this.archiveData = this.dataStore.map((file) => {
                return {
                    imageName: file.imageName,
                    filewordsName: file.filewordsName,
                    filewords: file.filewords,
                    labels: file.labels.map((label) => label),
                    imageDataUrl: file.imageDataUrl,
                    imageResizeUrl: file.imageResizeUrl,
                }
            });
        },
        differenceLabels(labels1, labels2) {
            let loss = [];
            let extra = [];
            labels1.forEach((label, index) => {
                if (!labels2.includes(label)) {
                    loss.push(index);
                }
            })
            labels2.forEach((label, index) => {
                if (!labels1.includes(label)) {
                    extra.push(index);
                }
            })
            return [loss, extra];
        },
        difference_data() {
            let difference_number = 0;
            let difference_data = [];
            for (let i = 0; i < this.archiveData.length; i++) {
                let archive = this.archiveData[i];
                let current = this.dataStore[i];
                let [loss, extra] = this.differenceLabels(archive.labels, current.labels);
                difference_number += loss.length + extra.length;
                let color_filewords_archive = archive.filewords;
                let color_filewords_current = current.filewords;
                loss.forEach((index) => {
                    color_filewords_archive = color_filewords_archive.replace(archive.labels[index], `<span style="color: red">${archive.labels[index]}</span>`)
                })
                extra.forEach((index) => {
                    color_filewords_current = color_filewords_current.replace(current.labels[index], `<span style="color: green">${current.labels[index]}</span>`)
                })
                if (loss.length + extra.length > 0)
                    difference_data.push([{
                        imageName: archive.imageName,
                        filewordsName: archive.filewordsName,
                        filewords: archive.filewords,
                        color_filewords: color_filewords_archive,
                        labels: archive.labels,
                        imageDataUrl: archive.imageDataUrl,
                        imageResizeUrl: archive.imageResizeUrl,
                        loss: loss,
                    }, {
                        imageName: current.imageName,
                        filewordsName: current.filewordsName,
                        filewords: current.filewords,
                        color_filewords: color_filewords_current,
                        labels: current.labels,
                        imageDataUrl: current.imageDataUrl,
                        imageResizeUrl: current.imageResizeUrl,
                        extra: extra,
                    }]);
            }
            return [difference_number, difference_data];
        },
        onLabelChooseChange() {
            let selected = false;
            for (let key in this.labelChoose) {
                if (this.labelChoose[key]) {
                    selected = true;
                    break;
                }
            }
            if (!selected) {
                this.visibleMask = this.visibleMask.map(() => true);
                return;
            }
            let labelsPositive = [];
            let labelsNegative = [];
            for (let key in this.labelChoose) {
                if (this.labelChoose[key])
                    if (!this.labelFilterStrategyTable[key]) {
                        labelsPositive.push(key);
                    } else {
                        labelsNegative.push(key);
                    }
            }
            this.visibleMask.forEach((mask, index) => {
                if (labelsPositive.length === 0 && labelsNegative.length !== 0)
                    this.visibleMask[index] = !this.includeLabels(this.dataStore[index].filewords, labelsNegative);
                else if (labelsNegative.length === 0 && labelsPositive.length !== 0)
                    this.visibleMask[index] = this.includeLabels(this.dataStore[index].filewords, labelsPositive);
                else
                    this.visibleMask[index] = this.includeLabels(this.dataStore[index].filewords, labelsPositive) && !this.includeLabels(this.dataStore[index].filewords, labelsNegative);
                if (this.negativeShow)
                    this.visibleMask[index] = !this.visibleMask[index];
            })
        },
        includeLabels(filewords, targetLabels) {
            let labels = this.getLabels(filewords);
            if (this.filterOperate) {
                for (let i = 0; i < targetLabels.length; i++) {
                    if (labels.includes(targetLabels[i])) {
                        return true;
                    }
                }
                return false;
            } else {
                for (let i = 0; i < targetLabels.length; i++) {
                    if (!labels.includes(targetLabels[i])) {
                        return false;
                    }
                }
                return true;
            }
        },
        getLabels(labelStr) {
            let labels = labelStr.split(', ');
            return labels.map((label) => {
                return label.replace(/^\x20*/, '').replace(/\x20*$/, '');
            })
        },
        updateLabels() {
            this.labelClassify = {};
            this.labelItemMap = {};
            this.labelChoose = {};
            this.labelFilterStrategyTable = {};
            this.visibleLabels = {};
            this.dataStore.forEach((item, index) => {
                const labels = this.getLabels(item.filewords);
                labels.forEach((label) => {
                    let key = label;
                    if (this.labelClassify.hasOwnProperty(key)) {
                        this.labelClassify[key]++;
                        this.labelItemMap[key].push(index);
                    } else {
                        this.labelClassify[key] = 1;
                        this.labelItemMap[key] = [index];
                        this.labelChoose[key] = false;
                        this.labelFilterStrategyTable[key] = false;
                        this.visibleLabels[key] = true;
                    }
                })
            })
        },
        simpleLabelCount(enabledIndex) {
            let labelClassify = {};
            enabledIndex.forEach((enable, index) => {
                if (enable) {
                    const labels = this.getLabels(this.dataStore[index].filewords);
                    labels.forEach((label) => {
                        let key = label;
                        if (labelClassify.hasOwnProperty(key)) {
                            labelClassify[key]++;
                        } else {
                            labelClassify[key] = 1;
                        }
                    })
                }
            })
            return labelClassify;
        },
        movableLabelCount(label, direction) {
            let result = 0;
            this.dataSelected.forEach((selected, index) => {
                if (selected) {
                    let labels = this.dataStore[index].labels;
                    let indexLabel = labels.indexOf(label);
                    if (indexLabel >= 0) {
                        if (direction === 'back' && indexLabel < labels.length - 1) {
                            result++;
                        } else if (direction === 'forward' && indexLabel > 0) {
                            result++;
                        }
                    }
                }
            })
            return result;
        },
        attachLabel(label) {
            this.dataSelected.forEach((selected, index) => {
                if (selected && this.dataStore[index].labels.indexOf(label) === -1) {
                    this.dataStore[index].labels.push(label);
                    this.dataStore[index].filewords += ', ' + label;
                }
            })
        },
        detachLabel(label) {
            this.dataSelected.forEach((selected, index) => {
                if (selected) {
                    let labels = this.dataStore[index].labels;
                    let indexLabel = labels.indexOf(label);
                    if (indexLabel >= 0) {
                        labels.splice(indexLabel, 1);
                    }
                    this.dataStore[index].filewords = '';
                    labels.forEach((label, i) => {
                        this.dataStore[index].filewords += label + (i < labels.length - 1 ? ', ' : '');
                    })
                }
            })
        },
        moveLabel(label, direction) {
            this.dataSelected.forEach((selected, index) => {
                if (selected) {
                    let labels = this.dataStore[index].labels;
                    let indexLabel = labels.indexOf(label);
                    if (indexLabel >= 0) {
                        if (direction === 'back' && indexLabel < labels.length - 1) {
                            labels.splice(indexLabel, 1);
                            labels.splice(indexLabel + 1, 0, label);
                        } else if (direction === 'forward' && indexLabel > 0) {
                            labels.splice(indexLabel, 1);
                            labels.splice(indexLabel - 1, 0, label);
                        }
                        this.dataStore[index].filewords = '';
                        labels.forEach((label, i) => {
                            this.dataStore[index].filewords += label + (i < labels.length - 1 ? ', ' : '');
                        })
                    }
                }
            })
        },
        setLabelPosition(label, position) {
            this.dataSelected.forEach((selected, index) => {
                if (selected) {
                    let labels = this.dataStore[index].labels;
                    let indexLabel = labels.indexOf(label);
                    if (indexLabel >= 0) {
                        labels.splice(indexLabel, 1);
                        labels.splice(Math.round(labels.length * position), 0, label);
                        this.dataStore[index].filewords = '';
                        labels.forEach((label, i) => {
                            this.dataStore[index].filewords += label + (i < labels.length - 1 ? ', ' : '');
                        })
                    }
                }
            })
        },
        updateLabelPosition(label) {
            let labelIndexList = [];
            let labelPositionList = [];
            this.dataSelected.forEach((selected, index) => {
                if (selected) {
                    let labels = this.dataStore[index].labels;
                    let indexLabel = labels.indexOf(label);
                    if (indexLabel >= 0) {
                        labelPositionList.push(indexLabel / (labels.length - 1));
                        labelIndexList.push(indexLabel);
                    }
                }
            })
            this.labelPositionOperationProtect = true;
            this.labelPosition = Math.round((labelPositionList.reduce((a, b) => a + b, 0) / labelPositionList.length * 100));
            this.labelPositionOperationProtect = false;
            this.averageLabelPosition = Math.round(labelIndexList.reduce((a, b) => a + b, 0) / labelIndexList.length);
        },
        addNewLabel() {
            if (this.newLabel === '') {
                this.$q.notify({message: 'Invalid label name', color: 'negative', position: 'top'})
                return;
            }
            if (this.labelClassify.hasOwnProperty(this.newLabel) || this.labelOptions.includes(this.newLabel)) {
                this.$q.notify({message: 'Label already exists', color: 'negative', position: 'top'})
                return;
            }
            this.labelOptions.push(this.newLabel);
            this.$q.notify({message: 'Label added', color: 'positive', position: 'top'})
            this.newLabel = '';
        },
        clearFilter() {
            for (let key in this.labelChoose) {
                this.labelChoose[key] = false;
            }
        },
        keySortByKey(dict) {
            return Object.keys(dict).sort();
        },
        keySortByValue(dict) {
            let keys = Object.keys(dict);
            keys.sort((a, b) => {
                return dict[b] - dict[a];
            })
            return keys;
        },
        labelsKeysSortByKey() {
            return this.keySortByKey(this.labelClassify);
        },
        labelsKeysSortByValue() {
            return this.keySortByValue(this.labelClassify);
        },
    },
    async mounted() {
        this.debug = this.$DEBUG
        if (this.debug) {
            this.base_url = 'http://localhost:5000'
        } else {
            this.base_url = '';
        }
        this.tagLoading = true;
        await this.getFiles();
        this.updateLabels();
        this.tagLoading = false;
        var app = this;
        document.addEventListener('keydown', function (event) {
            app.keyBoardTable[event.key] = true;
        });
        document.addEventListener('keyup', function (event) {
            app.keyBoardTable[event.key] = false;
        });
    },
    watch: {
        labelChoose: {
            handler: function (val, oldVal) {
                this.onLabelChooseChange();
            },
            deep: true
        },
        negativeShow: {
            handler: function (val, oldVal) {
                this.onLabelChooseChange();
            },
            deep: true
        },
        labelFilterStrategyTable: {
            handler: function (val, oldVal) {
                this.onLabelChooseChange();
            },
            deep: true
        },
        filterOperate: {
            handler: function (val, oldVal) {
                this.onLabelChooseChange();
            }
        },
        labelSearcher: {
            handler: function (val, oldVal) {
                for (let key in this.visibleLabels) {
                    this.visibleLabels[key] = key.includes(val);
                }
            },
            deep: true
        },
        selectedShow: {
            handler: function (val, oldVal) {
                if (val) {
                    this.visibleMask = this.dataSelected.map((selected) => selected);
                } else {
                    this.onLabelChooseChange();
                }
            },
            deep: true
        },
        labelOptions: {
            handler: function (value) {
                try {
                    if (value.length === 1) {
                        this.operateLabel = value[0];
                    }
                } catch (e) {
                    console.log(e);
                }
            },
            deep: true,
        },
        dataStore: {
            handler: function (value) {
                if (this.movableLabelCount(this.operateLabel, 'back') + this.movableLabelCount(this.operateLabel, 'forward') > 0 && !this.labelPositionOperationProtect) {
                    this.updateLabelPosition(this.operateLabel);
                }
            },
            deep: true,
        },
        labelPosition: {
            handler: function (value) {
                if (!this.labelPositionOperationProtect) {
                    //this.labelPositionOperationProtect = true;
                    // this.setLabelPosition(this.operateLabel, value / 100.0);
                    //this.labelPositionOperationProtect = false;
                }
            },
            deep: true,
        },
        dataSelected: {
            handler: function (value) {

            },
            deep: true,
        },
    }
})
</script>

<style>
.mask {
    background-image: linear-gradient(rgba(0, 0, 255, 0.3), rgba(0, 255, 255, 1));
    left: 0;
    opacity: 0.3;
    position: absolute;
    top: 0;
    z-index: 1;
    height: 100%;
    width: 100%;
    filter: alpha(opacity=50);
    pointer-events: none;
}

.maskT {
    background-color: transparent;
    left: 0;
    opacity: 0.9;
    position: absolute;
    top: 0;
    z-index: 2;
    height: 100%;
    width: 100%;
    pointer-events: none;
}
</style>
