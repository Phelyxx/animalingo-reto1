<template>
  <q-page padding>
    <p class="text-h6">¡Dale click al botón para analizar una imagen aleatoria!</p>
        <div class="col-12 text-center">
        <img src="" ref="imgTakePhoto" width="1000rem" style='width:100%;' border="0" alt="Null"/>
        <h5 ref="textField"></h5>
        <q-table
        :hide-no-data="true"
        title="Resultados"
        :data="posts"
        :columns="columns"
        row-key="name"
        class="col"
        />
      </div>
    <div class="row">
      <div class="col-12 text-center">
        <video autoplay width="250rem" ref="videoplay"></video>
      </div>
      <div class="col-12 text-center">
        <q-btn
          v-if="!obtainAnimal"
          label="Obtener animal"
          color="primary"
          icon="touch_app"
          :disable="!startRandom"
          @click="getRandom"
        />
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
      startRandom: false,
      obtainAnimal: false,
      imageCapture: null,
      track: null
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
      axios('http://127.0.0.1:8000/random')
        .then(response => {
          console.log(response.data[1])
          this.$refs.imgTakePhoto.src = response.data[2]
          const textField = this.$refs.textField
          textField.innerHTML = 'El animal es: ' + response.data[1]
          console.log(response.data[0])
          this.posts = response.data[0]
        })
        .catch(error => console.log('Error', error.message))
    }
  }
}
</script>
