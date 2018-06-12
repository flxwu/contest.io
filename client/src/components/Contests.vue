<template>
  <v-list style="max-height: 90%; overflow: scroll; width: 90%; margin: 0 auto; margin-top: 3%;">
    <v-card>
      <v-toolbar color="special1" dark>
        <v-toolbar-title>New public contests</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-list two-line>
        <v-list-tile v-for="contest in contests" :key="contest.contestcode">
          <v-list-tile-content>
            <v-list-tile-title>{{ contest.contestname }}</v-list-tile-title>
            <v-list-tile-sub-title>{{contest.tasks.length}} Problems</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-btn icon ripple>
              <v-icon color="grey lighten-1">info</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-card>
  </v-list>
</template>

<script>
import axios from 'axios';

export default {
  name: 'contests',
  components: {},
  data() {
    return {
      contests: []
    };
  },
  mounted() {
    axios.get("/api/contests?visible=1")
      .then(response => {
        this.contests = [response.data];
      })
      .catch(error => {
        alert(error);
      });
  },
  methods: {

  }
};

</script>
