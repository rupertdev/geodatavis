<template>
  <div id="app" class="container">
    <div class="row">

      <div class="col-md-12">
        <div id=map class=map>
        </div>
        <!-- The map goes here -->
      </div>


    </div>
  </div>
</template>

<script src='https://api.mapbox.com/mapbox.js/plugins/leaflet-heat/v0.1.3/leaflet-heat.js'></script>
<script>
import axios from 'axios';

export default {
  data () {
    return {
    map: null,
    tileLayer: null,
    layers: []
    }
  },
  mounted() {
    this.initMap();
    // this.initLayers();
  },
  methods: {
      initMap() {
        this.map = L.map('map').setView([38.63, -90.23], 12);

        this.tileLayer = L.tileLayer(
        'https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png',
        {
          maxZoom: 18,
          attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
        }
        );

        this.tileLayer.addTo(this.map);
        var heat = L.heatLayer(addressPoints, {maxZoom: 18}).addTo(map);
        this.map.on('load', this.get_data_for_bbox)
        this.map.on('moveend', this.get_data_for_bbox)
      },
      get_data_for_bbox(e) {
        map = e.target
        let bounds = map.getBounds();
        console.log(bounds)
        axios.post("http://localhost:5000/api/ipv4bbox", { "bbox": bounds })
        .then(function (response) {
          response.data.forEach(point => {
            console.log(point);
            heat.addLatLng(L.latLng(point['lat'], point['lng']));
          });
         });

      }
    }
  }
</script>

<style>
.map { height: 600px; }
</style>
