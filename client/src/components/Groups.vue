<template>
  <div id="wrapper">
      <v-container grow>
        <v-layout>
          <v-flex xs6 style="padding-right: 1%;">
            <v-list style="max-height: 65vh; overflow: hidden;">
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Groups you have joined</v-toolbar-title>
                  <v-spacer></v-spacer>
                </v-toolbar>
                <p v-if="!groups_joined.length" style="color: red; padding: 30px; font-size: 15pt;">
                  You have not joined any groups!
                </p>
                <v-list two-line v-else>
                  <v-list-tile v-for="group in groups_joined" :key="group.groupid">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ group.groupname }}</v-list-tile-title>
                      <v-list-tile-sub-title>{{ group.groupadmin }}</v-list-tile-sub-title>
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

            <v-dialog v-model="groupCreatePopup" max-width="500px">
              <v-card>
                <v-card-title>
                  Create new group
                </v-card-title>
                <v-card-text>
                  <v-text-field id="newGroupName" v-model="newGroupName" label="Group Name"></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-btn color="success" flat @click.stop="createGroup()">Create group</v-btn>
                  <v-btn color="error" flat @click.stop="groupCreatePopup=false">Close</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-list style="max-height: 65vh; overflow: hidden;">
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Groups you have created</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon ripple fab small @click="groupCreatePopup=!groupCreatePopup">
                    <v-icon>add</v-icon>
                  </v-btn>
                </v-toolbar>
                <p v-if="!groups_owned.length" style="color: red; padding: 30px; font-size: 15pt;">
                  You have not created any groups!
                </p>

                <v-list v-else two-line>
                  <v-list-tile v-for="group in groups_owned" :key="group.groupid">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ group.groupname }}</v-list-tile-title>
                      <v-list-tile-sub-title>{{ group.groupadmin }}</v-list-tile-sub-title>
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
  name: 'groups',
  components: {},
  data() {
    return {
      groupCreatePopup: false,
      newGroupName: '',
      groups_joined: [],
      groups_owned: []
    };
  },
  created: async function() {
    var groups_joined = [];
    // Get groups user is in
    await axios.get('/api/usergroup.memberships?admin=-1&user=' + localStorage.getItem('userid'))
      .then((response) => {
        if(response.data === null || typeof(response.data) === 'undefined') return;        
        groups_joined = response.data;
      });

    //Get groups user is admin/owner of
    await axios.get('/api/usergroup.memberships?admin=' + localStorage.getItem('userid') + '&user=' + localStorage.getItem('userid'))
      .then((response) => {
        if(response.data === null || typeof(response.data) === 'undefined') return;
        this.groups_owned = response.data;
      });

    // Remove all groups user is admin of from groups_joined
    this.groups_joined = groups_joined.filter(x => this.groups_owned[x]);
  },
  methods: {
    createGroup: async function() {
      let config = {
        headers: {
          'Content-Type': 'application/json'
        }
      };
      await axios.post('/api/usergroup', {
        'groupname': this.newGroupName,
        'groupadmin': localStorage.getItem('userid')
      }, config);
      this.groupCreatePopup = false;
    }
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
