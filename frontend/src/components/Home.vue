<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-md-12">
        <div id="map" class="map"></div>
        <!-- The map goes here -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      map: null,
      heat: null,
      tileLayer: null,
      layers: []
    };
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      this.map = L.map("map").fitWorld();

      this.tileLayer = L.tileLayer(
        "https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png",
        {
          maxZoom: 18,
          attribution:
            '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
        }
      );

      // Add tile and heatmap layers to the map
      this.tileLayer.addTo(this.map);
      this.heat = L.heatLayer([], { radius: 20 }).addTo(this.map);

      // Add event handlers to the map
      this.map.on("load", this.get_data_for_bbox);
      // this.map.on('zoomend', this.get_data_for_bbox)
      this.map.on("moveend", this.get_data_for_bbox);
    },
    get_data_for_bbox(e) {
      var latlngs = [];
      console.log("FIRED")
      // On move or load, request heatmap data from the DB
      self = this;
      axios
        .post('https://geodatavis.herokuapp.com/api/ipv4bbox', {
          bbox: e.target.getBounds()
        })
        .then(function(response) {
          response.data.forEach(point => {
            latlngs.push(L.latLng(point["lat"], point["lng"], point["count"]));
          });
          self.heat.setLatLngs(latlngs);
        });
    }
  }
};
</script>

<style>
.map {
  height: 100%;
  min-width: 80%;
}
.container {
  max-width: 90%;
}
.row {
  min-height: 800px;
}
</style>
