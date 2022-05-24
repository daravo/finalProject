let vueSearch = new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  data: {
    name: "",
    last_name: "",
    job: "",
    kword: "",
    lista_seleccionados: [],
    lista_workers: [123],
  },
  watch: {
    kword(val) {
      this.buscar_workers(val);
    },
  },
  methods: {
    buscar_workers: function (kword) {
      let url = "api/?kword=";
      let respuesta;
      fetch(url + kword)
        .then(function (response) {
          this.lista = response;
          console.log(respuesta);
        })
        .catch(function (error) {
          console.log(error);
        })
        .finally(() => {
          this.lista_workers = respuesta;
          console.log("trabajadores", this.lista_workers);
        });
    },
  },
});
