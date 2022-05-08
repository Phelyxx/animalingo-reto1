<template>
  <q-page padding>
    <p class="text-h6">¡Dale click al botón para analizar una imagen aleatoria!</p>
        <div class="q-pt-md col-12 text-center">
          <div class="q-gutter-md">
            <q-select v-model="category" :options="options" label="Seleccionar animal" ></q-select>
              <q-btn
                v-if="!obtainAnimal"
                label="Obtener animal"
                color="primary"
                icon="touch_app"
                @click="get_url_category"
              />
        <img src="" ref="imgTakePhoto" width="1000rem" style='width:100%;' border="0"/>
        <h5 ref="textField"></h5>
        <q-select v-model="model" :options="options_models" label="Seleccionar modelo"  v-if="seen" @click="get_table" ></q-select>
                <q-btn
                v-if="seen"
                label="Obtener tasas de acierto"
                color="primary"
                icon="touch_app"
                @click="get_table"
              />
        <q-table
        :hide-no-data="true"
        title="Resultados"
        :data="posts"
        :columns="columns"
        row-key="name"
        class="col"
        v-if="seen"
        />
      </div>
    </div>
    <div class="row">
      <div class="col-12 text-center">
        <video autoplay width="250rem" ref="videoplay"></video>
      </div>
    </div>
  </q-page>
</template>

<script>
const axios = require('axios')
export default {
  name: 'PageCamera',
  data () {
    return {
      columns: [
        {
          name: 'animal',
          label: 'Animal',
          field: 'animal',
          align: 'left',
          sortable: true
        },
        {
          name: 'porcentaje_confianza',
          label: 'Porcentaje Confianza',
          field: 'porcentaje_confianza',
          align: 'left',
          sortable: true
        }
      ],
      posts: [],
      seen: false,
      startRandom: false,
      obtainAnimal: false,
      imageCapture: null,
      track: null,
      category: 'dikdik',
      model: 'SIN PCA',
      options: ['baboon', 'buffalo', 'elephant', 'gazellegrants', 'gazellethomsons', 'giraffe', 'guineafowl', 'hartebeest', 'hippopotamus', 'hyenaspotted', 'impala', 'lionfemale', 'otherbird', 'reedbuck', 'topi', 'warthog', 'wildebeest', 'zebra'
      ],
      options_models: [
        'SIN PCA', 'CON PCA'
      ]
    }
  },
  mounted () {
    if (navigator.mediaDevices.getUserMedia) {
      this.startRandom = true
    }
  },
  methods: {
    getRandom () {
      console.log('xd')
      axios('https://swift-cobras-call-201-245-212-13.loca.lt/random')
        .then(response => {
          console.log(response.data[1])
          this.$refs.imgTakePhoto.src = response.data[2]
          const textField = this.$refs.textField
          textField.innerHTML = 'El animal es: ' + response.data[1]
          console.log(response.data[0])
          this.posts = response.data[0]
          this.seen = true
          console.log(this.animal)
        })
        .catch(error => console.log('Error', error.message))
    },
    get_url_category () {
      axios('http://large-schools-teach-201-245-212-13.loca.lt/random/?animal=' + this.category)
        .then(response => {
          console.log(response.data)
          this.$refs.imgTakePhoto.src = response.data
          this.seen = true
        })
        .catch(error => console.log('Error', error.message))
    },
    get_table () {
      axios('http://large-schools-teach-201-245-212-13.loca.lt/table/?pca=' + this.model.slice(0, 3))
        .then(response => {
          this.posts = response.data
        })
        .catch(error => console.log('Error', error.message))
    }
  }
}
</script>
