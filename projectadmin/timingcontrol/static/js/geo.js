//proyecto
Vue.component("proyecto", {
  delimiters: ["[[", "]]"],
  template: "#proyecto-template",
  props: ["datos"],
  data(){
    return{
      fecha: "",
      hora: "",
      project_selected: "",
    }  
  },
  methods: {
    guardarhora(project, idproject){
      console.log('entra en guardarhora del componente');
      let fecha = new Date();
      let dia = fecha.getDate();
      if (dia<10){
        dia = '0'+dia;
      }
      let mes = fecha.getMonth()+1;
      if (mes<10){
        mes = '0'+mes;
      }
      let anio = fecha.getFullYear();
      this.fecha = anio+'-'+mes+'-'+dia;

      //Obtener hora:
      let hora = fecha.getHours();
      if (hora<10){
        hora = '0'+hora;
      }
      let minutos = fecha.getMinutes();
      if (minutos<10){
        minutos = '0'+minutos;
      }
      let segundos = fecha.getSeconds();
      if (segundos<10){
        segundos = '0'+segundos;
      }
      this.hora = hora+':'+minutos+':'+segundos;
      this.project_selected = project;
      this.$root.project_selected = project;
      this.$root.id_project_selected = idproject;
      console.log('fecha guardada', this.fecha, 'hora guardada',this.hora);  
    },
  },
  mounted() {
    console.log(this.datos)
  }
});
let geo = new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  data: {
    message: "Hola Vue!",
    fecha: "fecha",
    hora: "",
    latitud: "",
    longitud: "",
    accuracy: "",
    check_in: false,
    check_out: false,
    projects: new Array(), //lleno con un array de objetos con los proyectos
    project_around: [], //Proyectos alrededor de la posición actual
    project_selected: '',
    id_project_selected: "",
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
      this.guardarhora();
  },
  methods: {
    guardarhora(){
      console.log('entra en guardarhora del root');
      let fecha = new Date();
      let hour = fecha.getTime();
      let dia = fecha.getDate();
      let anio = fecha.getFullYear();
      if (dia<10){
        dia = '0'+dia;
      }
      let mes = fecha.getMonth()+1;
      if (mes<10){
        mes = '0'+mes;
      }
      this.fecha = anio+'-'+mes+'-'+dia;
      //Obtener hora:
      let hora = fecha.getHours();
      if (hora<10){
        hora = '0'+hora;
      }
      let minutos = fecha.getMinutes();
      if (minutos<10){
        minutos = '0'+minutos;
      }
      let segundos = fecha.getSeconds();
      if (segundos<10){
        segundos = '0'+segundos;
      }
      this.hora = hora+':'+minutos;

      console.log('fecha guardada', this.fecha, 'hora guardada',this.hora);
    },
    geolocalizar: function () {
      console.log("mallamao");
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          this.success(position);
          this.guardar_variables(
            position.coords.latitude,
            position.coords.accuracy,
            position.coords.longitude
          );

        }, (positionErrorCallback) => { console.log(error) }, { enableHighAccuracy: true });
        console.log("final del if");

      }
    },
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
//modificar para pruebas el valor de la distancia
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
