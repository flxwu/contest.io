<template>
  <div id="navbar">

    <!-- Toolbar -->
    <v-toolbar>
      <!-- Side Bar Icon -->
      <v-toolbar-side-icon></v-toolbar-side-icon>

      <router-link to="/" tag="v-toolbar-title" class="titlenavbar">Contest.io</router-link>

      <v-spacer></v-spacer>

      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn to="/dashboard" flat>Dashboard</v-btn>
        <v-btn flat href="http://localhost:5000/api/github-logout" v-if="loggedIn">Logout</v-btn>
        <v-btn flat @click="loginDialog=true" v-if="!loggedIn">Login</v-btn>
        <v-dialog v-model="loginDialog" max-width="500px">
        <v-card>
          <v-card-title>
            Login
          </v-card-title>
          <v-card-text>
            <v-btn color="grey darken-4" style="color: white" href="http://localhost:5000/api/github-login"><span style="font-size: 2em; margin-right: 10px;"><i class="fab fa-github"></i></span> Login with Github</v-btn>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="loginDialog=false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      </v-toolbar-items>

    </v-toolbar>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'navbar',
  components: {

  },
  data() {
    return {
      loginDialog: false,
      github: "",
      loggedIn: false,
      user: {}
    }
  },
  // See if a user is logged in
  created: function () {
    axios.get("http://localhost:5000/api/github-user")
    .then(resp => {
      if(!(resp.data == "401: Bad credentials")) {
        this.loggedIn = true
        this.user = resp.data
        console.log(resp)
      }
    })
  }
}
</script>

<style scoped>
.titlenavbar:hover {
  cursor: pointer;
}
</style>
