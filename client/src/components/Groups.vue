<template>
  <div id="wrapper">
      <v-container grow>
        <v-layout>
          <v-flex xs6 style="padding-right: 1%;">
            <v-list>
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Groups you have joined</v-toolbar-title>
                  <v-spacer></v-spacer>
                </v-toolbar>
                <v-list two-line>
                  <v-list-tile v-for="group in groups_joined" :key="group.groupid">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ group.groupname }} - 20 Members</v-list-tile-title>
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

            <v-list style="max-height: 70%; overflow: scroll;">
              <v-card>
                <v-toolbar color="special1" dark>
                  <v-toolbar-title>Groups you have created</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon ripple fab small @click="groupCreatePopup=!groupCreatePopup">
                    <v-icon>add</v-icon>
                  </v-btn>
                </v-toolbar>
                <v-list two-line>
                  <v-list-tile v-for="group in groups_owned" :key="group.groupid">
                    <v-list-tile-content>
                      <v-list-tile-title>{{ group.groupname }} - 20 Members</v-list-tile-title>
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
      groups_joined: [{groupid: 1, groupname: 'Nicegroup', groupadmin: 'flxwu'}],
      groups_owned: [{groupid: 1, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 2, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 3, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 4, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 5, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 6, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 7, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 8, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 9, groupname: 'Awesomegroup', groupadmin: 'Qo2770'},{groupid: 10, groupname: 'Awesomegroup', groupadmin: 'Qo2770'}]
    };
  },
  created: () => {
    // Get groups user is in
    axios.get('/api/user');

    // Get groups user is admin/owner of
    axios.get();
  },
  methods: {
    createGroup() {
      let config = {
        headers: {
          'Content-Type': 'application/json'
        }
      };
      axios.post('/api/usergroup', {
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
