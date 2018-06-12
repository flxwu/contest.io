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
              </div>
            </v-card-title>

          </v-card>
        </v-flex>

        <v-flex xs9>
          <v-tabs grow icons-and-text centered dark color="primary">
            <v-tabs-slider color="white"></v-tabs-slider>
            <v-tab ripple>
              Groups
              <v-icon>group</v-icon>
            </v-tab>
            <v-tab ripple>
              Contests
              <v-icon>list</v-icon>
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
    if(localStorage.getItem('userid') != -1 || localStorage.getItem('userid') != null) {
      this.user = JSON.parse(localStorage.getItem('data'));
      console.log(this.user);
    } else {
      window.location = history.go(-1);
    }
  }
};
</script>

<style scoped>

</style>
