<template>
  <div id="wrapper">
      <v-container grow>
        <v-layout>
          <v-flex xs6 style="padding-right: 1%;">
            <v-list>
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Contests you have joined</v-toolbar-title>
                  <v-spacer></v-spacer>
                </v-toolbar>
                <p v-if="!contests_joined.length" style="color: red; padding: 29px; font-size: 15pt;">
                  You have not joined any contests!
                </p>
                <v-list v-else two-line>
                  <v-list-tile v-for="contest in contests_joined" :key="contest.contestcode" :to="'contest/' + contest.contestcode">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ contest.contestname }}</v-list-tile-title>
                      <v-list-tile-sub-title>Ends on {{contest.date_end | moment("dddd, MMMM Do YYYY") }} ({{contest.date_end | moment("from", true) }})</v-list-tile-sub-title>
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
          </v-flex>

          <v-flex xs6 style="padding-left: 1%;">

            <v-list style="max-height: 50vh; overflow: hidden;">
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Contests you have created</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon ripple fab small to="/contestcreate">
                    <v-icon>add</v-icon>
                  </v-btn>
                </v-toolbar>
                <p v-if="!contests_owned.length" style="color: red; padding: 29px; font-size: 15pt;">
                  You have not created any contests!
                </p>
                <v-list v-else two-line>
                  <v-list-tile v-for="contest in contests_owned" :key="contest.contestcode" :to="'contest/' + contest.contestcode">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ contest.contestname }}</v-list-tile-title>
                      <v-list-tile-sub-title>Ends on {{contest.date_end | moment("dddd, MMMM Do YYYY") }} ({{contest.date_end | moment("from", true) }})</v-list-tile-sub-title>
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
          </v-flex>
        </v-layout>
      </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'contestsoverview',
  components: {},
  data() {
    return {
      contests_owned: [],
      contests_joined: []
    };
  },
  async created() {
    var contests = [];
    await axios.get("/api/contests.joined?user=" + localStorage.getItem('userid'))
      .then(response => {
        if(response.data === null || typeof(response.data) === 'undefined') return                
        contests = Array.isArray(response.data) ? response.data : [response.data];
        for (var i = 0; i < contests.length; i++) {
          axios.get("/api/contest?code=" + contests[i].contest)
            .then((response) => {
              this.contests_joined.push(response.data);
            }
          );
        }
      }
    );

    await axios.get("/api/contests?admin=" + localStorage.getItem('userid'))
      .then((response) => {
        if(response.data === null || typeof(response.data) === 'undefined') return                
        this.contests_owned = response.data;
      }
    );
  },
  methods: {

  }
};

</script>

<style scoped>
#wrapper {
  background: white;
  min-height: 60vh;
  max-height: 60vh;
}
</style>
