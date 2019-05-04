<template>
  <div id="app">
    <MapView></MapView>
    <!--    <div id="nav">-->
    <!--      <router-link to="/">Home</router-link> |-->
    <!--      <router-link to="/about">About</router-link>-->
    <!--    </div>-->
    <!--    <router-view/>-->
  </div>
</template>

<style>

  html, body {
    height: 100%;
    margin: 0px;
    padding: 0px;
  }

  #app {
    height:100%;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }


</style>
<script>
  import MapView from "@/components/MapView";

  export default {
    components: {MapView}
  }
</script>
