<template>
  <div id="app">
    <!-- all elements need to be enclosed in v-app tags -->
    <v-app>
      <NavBar></NavBar>

      <v-content>
        <v-container fluid>
          <router-view></router-view>
        </v-container>
      </v-content>

      <Footer app></Footer>

    </v-app>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'app',
  components: {
    NavBar, Footer
  }
};
</script>

<style>
#app {
  font-family: 'Exo 2', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: 100%;
}

Footer {
  z-index: 1;
  position: relative;
  bottom: 0;
  width: 100%;
}

</style>
