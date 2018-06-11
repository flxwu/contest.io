<template>
  <div>
    <!-- Layout container -->
    <v-container fluid>

      <v-layout>

        <v-flex xs3 style="margin-right: 3%">
          <v-card class="cardprofile">

            <v-card-title primary-title>
              <div  style="width: 100% !important">
                <h3 class="headline mb-0">Profile</h3>
                <v-divider></v-divider><br>
                <v-avatar size="128px"><img :src="user.avatar_url" alt="avatar"></v-avatar><br><br>
                <div>Username:  {{ user.login }}  ({{ user.name }})</div>
                <div>Email:  {{ user.email }} </div><br>
                <div>{{ user.bio }} </div><br>
              </div>
            </v-card-title>

          </v-card>
        </v-flex>

        <v-flex xs9>
          <v-tabs grow icons-and-text centered dark color="primary">
            <v-tabs-slider color="white"></v-tabs-slider>
            <v-tab
              v-for="n in 2"
              :key="n"
              ripple
            >
              Item {{ n }}
            </v-tab>
            <v-tab-item>
              <Groups />
            </v-tab-item>
            <v-tab-item>
              <Contests />
            </v-tab-item>
          </v-tabs>
        </v-flex>

      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

import Groups from './Groups.vue';
import Contests from './ContestsOverview.vue';

export default {
  name: 'dashboard',
  components: {
    Groups, Contests
  },
  data() {
    return {
      user: {},
      id: null,
      texts: ['Hi', 'Moin', 'Holl']
    };
  },
  // See if a user is logged in
  created: function () {
    axios.get('/api/github-user')
      .then(resp => {
        if(!(resp.data == '401: Bad credentials')) {
          this.user = resp.data.ghdata;
          this.id = resp.data.id;
          localStorage.setItem('userid', this.id);
          console.log(resp.data);
        } else {
          window.location = history.go(-1);
        }
      });
  }
};
</script>

<style scoped>

</style>
