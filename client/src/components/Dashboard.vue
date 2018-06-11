<template>
  <div>
    <!-- Layout container -->
    <v-container fluid>

      <v-layout>

        <v-flex xs3>
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

        </v-flex>

      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'dashboard',
  components: {},
  data() {
    return {
      user: {}
    };
  },
  // See if a user is logged in
  created: function () {
    axios.get('/api/github-user')
      .then(resp => {
        if(!(resp.data == '401: Bad credentials')) {
          this.user = resp.data;
          console.log(this.user);
        } else {
          window.location = history.go(-1);
        }
      });
  }
};
</script>

<style scoped>

</style>
