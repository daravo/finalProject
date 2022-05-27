//proyecto
Vue.component("proyecto", {
  delimiters: ["[[", "]]"],
  template: "#proyecto-template",
  props: ["datos"],
  mounted() {
    console.log(this.datos)
  }
});
let geo = new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  data: {
    message: "Hola Vue!",
    latitud: "",
    longitud: "",
    accuracy: "",
    check_in: false,
    check_out: false,
    projects: new Array(), //lleno con un array de objetos con los proyectos
    project_around: [], //Proyectos alrededor de la posición actual
  },
  watch: {
    latitud: function () {
      return this.latitud
    },
    projects() {
      return this.projects
    }
  },
  mounted() {
    axios
      .get("api/projects")
      .then(
        (response) =>
          (this.projects = response.data))
      .catch((error) => console.log(error));
  },
  methods: {
    capturarHora() {
      console.log('entra en captura de hora');

    },

    geolocalizar: function () {
      console.log("mallamao");
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {

          this.guardar_variables(
            position.coords.latitude,
            position.coords.accuracy,
            position.coords.longitude
          );
          this.success(position);
        });
        console.log("final del if");
       
      }
    },
    /* doSomething: function () {
       console.log("entra al something");
       const watchID = navigator.geolocation.watchPosition((position) => {
         this.guardar_variables(
           position.coords.latitude,
           position.coords.accuracy,
           position.coords.longitude
         );
       });
     },*/
    guardar_variables: function (lat, acc, lon) {
      this.latitud = lat;
      this.longitud = lon;
      this.accuracy = acc;
      console.log(lat, "axx: " + acc, lon);
      this.rellenar_proyectos(lat, lon);
    },
    rellenar_proyectos: function (latitud, longitud) {
      let arrayAux = new Array();
      console.log('lee proyectos', this.projects);
      this.projects.forEach((element) => {
        const R = 6371; //KM radio tierra
        let latlong = element.lat_long.split(",");
        //paso a radianes:
        let lat = (parseFloat(latlong[0]) * Math.PI) / 180;
        let long = (parseFloat(latlong[1]) * Math.PI) / 180;
        let lat2 = (latitud * Math.PI) / 180;
        let lon2 = (longitud * Math.PI) / 180;
        //Diferencia entre latitudes y longitudes:
        let difLat = lat2 - lat;
        let difLon = lon2 - long;
        let formula =
          Math.sin(difLat / 2) * Math.sin(difLat / 2) +
          Math.sin(difLon / 2) *
          Math.sin(difLon / 2) *
          Math.cos(lat) *
          Math.cos(lat2);
        let formula2 =
          2 * Math.atan2(Math.sqrt(formula), Math.sqrt(1 - formula));

        let distancia = R * formula2;
        console.log("distancia", distancia);

        if (distancia <= 0.900 && this.project_around.indexOf(element) == -1) { //Distancia menor a 300 metros, para pruebas en ordenador, menor de 700
          this.project_around.push(element);
        }
      });
      console.log('arrayAuxiliar', arrayAux);
      console.log("proyectos cercanos", this.project_around);
    },
    success(position) {
      var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
      var myOptions = {
        zoom: 15,
        center: latlng,
        mapTypeControl: false,
        navigationControlOptions: { style: google.maps.NavigationControlStyle.SMALL },
        mapTypeId: google.maps.MapTypeId.ROADMAP
      }
      var map = new google.maps.Map(document.getElementById("mapcanvas"), myOptions)
      var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: "Estás aquí! (en un radio de " + position.coords.accuracy + " metros)"
      })
    },
  },
});
