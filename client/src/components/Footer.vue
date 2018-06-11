<template>
  <v-footer height="auto" class="grey darken-3">
    <v-layout row wrap justify-center>
      <v-btn
        v-for="link in links"
        :key="link"
        color="white"
        flat
        :to="link.url"
      >
        {{ link.title }}
      </v-btn>
      <v-flex xs12 py-3 text-xs-center white--text>
        &copy;2018 — <strong>contest.io</strong>
      </v-flex>
    </v-layout>
  </v-footer>
</template>

<script>

export default {
  name: 'footer',
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
}

</script>
