<template>
    <q-layout view="lHh Lpr lFf">
        <q-header elevated>
            <q-toolbar>
                <q-btn
                    flat
                    dense
                    round
                    icon="menu"
                    aria-label="Menu"
                    @click="toggleLeftDrawer"
                />

                <q-toolbar-title>
                    LabelEditor
                </q-toolbar-title>
                <q-select
                    v-model="locale"
                    :options="localeOptions"
                    label="Language Switcher"
                    dense
                    borderless
                    emit-value
                    map-options
                    options-dense
                    style="min-width: 150px"
                />
<!--                <div>Quasar v{{ $q.version }}</div>-->
            </q-toolbar>
        </q-header>

        <q-page-container>
            <router-view/>
        </q-page-container>
    </q-layout>
</template>

<script>
import {defineComponent, ref} from 'vue'


export default defineComponent({
    name: 'MainLayout',

    components: {},

    methods: {
        getCookieLocale(){
           let locale =  this.$q.cookies.get('locale')
            if (locale === undefined || locale === null) {
                let browserLang = navigator.language || navigator.userLanguage;
                if (this.localeOptions.map(item => item.value).includes(browserLang)) {
                    locale = browserLang
                } else {
                    locale = 'en-US'
                }
                this.$q.cookies.set('locale', locale)
            }
            return locale
        },
        setCookieLocale(locale){
            this.$q.cookies.set('locale', locale)
        }
    },

    data: () => {
        return {
            locale: 'zh-CN',
            localeOptions: [
                {value: 'zh-CN', label: '中文'},
                {value: 'en-US', label: 'English'}
            ]
        };
    },

    mounted() {
        this.locale = this.getCookieLocale()
        this.$i18n.locale = this.locale
    },

    watch:{
        locale: function (newLocale) {
            this.setCookieLocale(newLocale)
            this.$i18n.locale = newLocale
        }
    },

    setup() {
        const leftDrawerOpen = ref(false)
        // const { locale } = useI18n()

        return {
            // locale,
            leftDrawerOpen,
            toggleLeftDrawer() {
                leftDrawerOpen.value = !leftDrawerOpen.value
            }
        }
    }
})
</script>
