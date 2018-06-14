<template>
  <v-list style="max-height: 90%; width: 90%; margin: 0 auto; margin-top: 3%;">
    <v-card>
      <v-toolbar color="special1" dark>
        <v-toolbar-title>New public contests</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-list two-line>
        <p v-if="!contests.length" style="color: red; padding: 29px; font-size: 15pt;">
          There are no public contests available. Go an create one!
        </p>
        <v-list-tile v-else v-for="contest in contests" :key="contest.contestcode" :to="'contest/' + contest.contestcode">
          <v-list-tile-content>
            <v-list-tile-title>{{ contest.contestname }}</v-list-tile-title>
            <v-list-tile-sub-title>Ends on {{contest.date_end | moment("dddd, MMMM Do YYYY") }} ({{contest.date_end | moment("from", true) }})</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-btn icon ripple>
              <v-icon color="grey lighten-1">go</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-card>
  </v-list>
</template>

<script>
import axios from 'axios';
// eslint-disable-next-line
import moment from 'vue-moment'

export default {
  name: 'contests',
  components: {},
  data() {
    return {
      contests: []
    };
  },
  mounted() {
    axios.get('/api/contests?visible=1')
      .then(response => {
        if(response.data === null || typeof(response.data) === 'undefined') return;
        this.contests = Array.isArray(response.data) ? response.data : [response.data];
      })
      .catch(error => {
        alert(error);
      });
  },
  methods: {

  }
};

</script>
