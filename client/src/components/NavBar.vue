<template>
  <div id="navbar">

    <!-- Toolbar -->
    <v-toolbar dark color="primary">
      <!-- Side Bar Icon -->
      <v-toolbar-side-icon @click="drawer = true"></v-toolbar-side-icon>

      <router-link to="/" tag="v-toolbar-title" class="titlenavbar">Contest.io</router-link>

      <v-spacer></v-spacer>

      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn to="/dashboard" flat v-if="loggedIn">Dashboard</v-btn>
        <v-btn flat href="/api/github-logout" @click="logOut()" v-if="loggedIn">Logout</v-btn>
        <v-btn flat @click="loginDialog=true" v-if="!loggedIn">Login</v-btn>
        <v-dialog v-model="loginDialog" max-width="500px">
        <v-card>
          <v-card-title>
            Login
          </v-card-title>
          <v-card-text>
            <v-btn color="grey darken-4" style="color: white" href="/api/github-login"><span style="font-size: 2em; margin-right: 10px;"><i class="fab fa-github"></i></span> Login with Github</v-btn>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="loginDialog=false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      </v-toolbar-items>

    </v-toolbar>

    <!-- Navigation sidebar -->

    <v-navigation-drawer
      v-model="drawer"
      temporary
      dark
      absolute
    >
      <v-list class="pt-0" dense>
        <v-toolbar flat>
          <v-list>
            <v-list-tile>
              <v-list-tile-title class="title">
                Navigation
              </v-list-tile-title>
              <v-btn small flat fab style="float: right; margin-top: 10px;" @click.stop="drawer = false">
                <v-icon>chevron_left</v-icon>
              </v-btn>
            </v-list-tile>
          </v-list>
        </v-toolbar>
        <v-divider light></v-divider>
        <v-list-tile v-for="link in links" :key="link.title" :to="link.url">
          <v-list-tile-action>
            <v-icon>arrow_right</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ link.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "navbar",
  components: {},
  data() {
    return {
      loginDialog: false,
      github: "",
      loggedIn: false,
      user: {},
      drawer: false,
      userid: null,
      links: [
        { title: "Home", url: "/" },
        { title: "Contests", url: "contests" }
      ]
    };
  },
  // See if a user is logged in
  mounted: function() {
    if (localStorage.getItem("userid") != -1) {
      this.loggedIn = true;
    } else {
      axios.get("/api/github-user").then(resp => {
        if (!(resp.data == "401: Bad credentials")) {
          console.log(resp);
          this.loggedIn = true;
          this.user = resp.data.ghdata;
          this.userid = resp.data.id;
          localStorage.setItem("userid", this.userid);
          localStorage.setItem("data", JSON.stringify(this.user));
        }
      });
    }
  },
  methods: {
    logOut() {
      this.loggedIn = false;
      localStorage.setItem("userid", -1);
      localStorage.setItem("data", null);
    }
  }
};
</script>

<style>
.titlenavbar:hover {
  cursor: pointer;
}
</style>
