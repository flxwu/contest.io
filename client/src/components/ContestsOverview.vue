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
                <v-list two-line>
                  <v-list-tile v-for="contest in contest_joined" :key="contest.contestcode">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ contest.contestname }}</v-list-tile-title>
                      <v-list-tile-sub-title>{{length(contest.tasks)}} Problems</v-list-tile-sub-title>
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

            <v-list style="max-height: 70%; overflow: scroll;">
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Contests you have created</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon ripple fab small to="/contestcreate">
                    <v-icon>add</v-icon>
                  </v-btn>
                </v-toolbar>
                <v-list two-line>
                  <v-list-tile v-for="contest in contests_owned" :key="contest.contestcode">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ contest.contestname }}</v-list-tile-title>
                      <v-list-tile-sub-title>{{length(contest.tasks)}} Problems</v-list-tile-sub-title>
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
      contests_owned: [{}]
    };
  },
  created: () => {
    axios.get("/api/contest?admin")
      .then(response => {
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
  min-height: 68vh;
  max-height: 68vh;
}
</style>
