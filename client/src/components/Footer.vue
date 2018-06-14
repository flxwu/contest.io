<template>
  <v-footer height="inherit" class="grey darken-3">
    <v-layout row wrap justify-center>
      <v-btn
        v-for="link in links"
        :key="link.title"
        color="white"
        flat
        :to="link.url"
      >
        {{ link.title }}
      </v-btn>
      <v-flex xs12 py-3 text-xs-center white--text>
        &copy;2018 — <strong>contest.io (<a href="http://quentin-oschatz.me" target="_blank">Quentin Oschatz</a> and <a href="https://flxwu.com" target="_blank">Felix Wu</a>)</strong>
      </v-flex>
    </v-layout>
  </v-footer>
</template>

<script>

export default {
  name: 'footer_',
  components: {

  },
  data() {
    return {
      links: [
        { title: 'Home', url: '/' },
        { title: 'Contests', url: 'contests' }
      ]
    };
  },
};

</script>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}
a:hover {
  color: #26A69A;
}
</style>
