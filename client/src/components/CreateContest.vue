<template>
  <div id="createcontest">
    <!-- Layout container -->
    <v-container>
      <!-- Required field alerts -->
      <v-alert
        :value="alertTask"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        At least one task must be selected!
      </v-alert>

      <v-alert
        :value="alertDate"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        An ending date for the contest must be selected!
      </v-alert>

      <v-alert
        :value="alertName"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        A name for the contest must be entered!
      </v-alert>

      <v-alert
        :value="alertAxios"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        An error occured when attempting to create contest! ( {{ this.axiosError }} )
      </v-alert>

      <v-form>
        <v-layout>

          <!-- Add tasks -->
          <v-flex xs10 id="taskselection">
            <v-text-field prepend-icon="search" v-model="searchtitle" label="Search by name" solo-inverted class="mx-0 search" clearable flat></v-text-field>
            <div style="width: 100%;">
              <v-select style="float: right; width: 50%; margin-top: -32px;" v-model="selectedtags" label="Search by tags" chips tags solo prepend-icon="filter_list" append-icon="" clearable>
                <template slot="selection" slot-scope="data">
                  <v-chip :selected="data.selected" close @input="removeSelectedTag(data.item)" >
                    <span>{{ data.item }}</span>&nbsp;
                  </v-chip>
                </template>
              </v-select>
            </div>
            <div style="height: 320px; overflow: scroll; margin-top: 40px; min-width: 100%;">
              <v-list>

                <template v-if="!filteredItems.length">

                  <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>

                  <v-list-tile-content v-else>
                     <v-list-tile-title style="color: red; text-align: center;">No tasks match search parameters!</v-list-tile-title>
                  </v-list-tile-content>

                </template>

                <template v-for="item in filteredItems">

                  <!-- Detail view popup -->
                  <v-dialog v-model="detailPopup" max-width="500px" :key="item.taskid + '-popup'">
                    <v-card>
                      <v-card-title>
                        Detail
                      </v-card-title>
                      <v-card-text>
                        {{ item.taskname }}<br>
                        <small style="margin-right: 10px; float: left; margin-top: 8px; margin-left: 40%;">Difficulty ({{ item.codeforces_index }}): </small>
                        <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="width: 50px; margin-right: 50px; float: left;" value="20" buffer-value="20" color="green"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="width: 50px; margin-right: 50px; float: left;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="width: 50px; margin-right: 50px; float: left;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="width: 50px; margin-right: 50px; float: left;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                        <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="width: 50px; margin-right: 50px; float: left;" value="100" color="red"></v-progress-linear>
                        <v-progress-linear v-else style="width: 50px; margin-right: 50px; float: left;" value="100" color="red"></v-progress-linear><br>

                      </v-card-text>

                      <!-- Tags -->
                      <div class="text-xs-center chiptag">
                        <v-chip :key="tag" small v-for="tag in item.tasktags" >{{ tag }}</v-chip>
                      </div>

                      <v-card-actions>

                        <v-btn flat color="orange" :href="item.codeforces_url" target="blank">Preview</v-btn>
                        <v-btn color="primary" flat @click.stop="detailPopup=false">Close</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                   <v-list-tile avatar :key="item.taskid + '-avatar2'" @click="() => {}">

                     <v-list-tile-action>
                         <v-icon @click="addTask(item.taskid)">add</v-icon>
                     </v-list-tile-action>

                    <v-list-tile-content @click="detailPopup=true">
                       <v-list-tile-title v-html="item.taskname"></v-list-tile-title>
                    </v-list-tile-content>

                    <small style="position: absolute; left: 380px;">Difficulty ({{ item.codeforces_index }}): </small>
                    <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                    <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="position: absolute; left: 465px; top: 12px; width: 50px;" value="100" color="red"></v-progress-linear>
                    <v-progress-linear v-else style="position: absolute; left: 465px; top: 12px; width: 50px;" value="100" color="red"></v-progress-linear>

                    <v-chip :key="tag" small v-for="tag in item.tasktags.slice(0, 2)" >{{ tag }}</v-chip>

                   </v-list-tile>

                   <v-divider :key="item.taskid + '-divider'"></v-divider>

                 </template>

             </v-list>
            </div>

            <!-- Task list -->
            <v-subheader style="margin-top: 5%;"> Tasks Selected so far </v-subheader>

            <p v-if="!tasks.length" style="color: red;">No tasks selected! Browse above tasks and click the '+' icon to add them!</p>
            <v-expansion-panel popout>

             <v-expansion-panel-content v-for="item in tasks" :key="item.id">

               <div slot="header">
                  {{ item.taskname }}<br>
                  <small style="float: left; margin-top: 9px; margin-right: 10px;">Difficulty ({{ item.codeforces_index }}): </small>
                   <v-progress-linear v-if="item.codeforces_index.split('')[0] === 'A'" style="float:left; width: 50px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'B'" style="float:left; width: 50px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'C'" style="float:left; width: 50px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'D'" style="float:left; width: 50px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                   <v-progress-linear v-else-if="item.codeforces_index.split('')[0] === 'E'" style="float:left; width: 50px;" value="100" color="red"></v-progress-linear>
                   <v-progress-linear v-else style="float:left; width: 50px;" value="100" color="red"></v-progress-linear>
               </div>

              <v-card>



                <!-- Tags -->
                <div class="text-xs-center chiptag">
                  <v-chip :key="tag" small v-for="tag in item.tasktags" >{{ tag }}</v-chip>
                </div>

                <v-card-actions>
                  <v-btn flat color="red" @click="removeTask(item.taskid)">Remove</v-btn>
                  <v-btn flat color="orange" :href="item.codeforces_url" target="blank">Preview</v-btn>
                </v-card-actions>

              </v-card>

             </v-expansion-panel-content>

           </v-expansion-panel>
          </v-flex>

          <!-- Divider -->
          <v-flex xs1></v-flex>

          <!-- Misc Setup (Start / End time), Groups, etc. -->
          <v-flex xs4>
            <v-card>
              <v-card-text>
                <p v-if="contestdate">Contest End: {{ contestdate | moment("dddd, MMMM Do YYYY") }} (23:59)</p>
                <v-btn small color="primary" dark @click.stop="dialog2 = true">Choose a date...*</v-btn>

                <v-dialog v-model="dialog2" max-width="500px">
                  <v-card>
                    <v-card-title>
                      Choose an end date for the contest
                    </v-card-title>
                    <v-card-text>
                      <v-date-picker v-model="contestdate" :min="now"></v-date-picker><br>
                      <small>Note: Contests always end at 23:59!</small>
                    </v-card-text>
                    <v-card-actions>
                      <v-btn color="primary" flat @click.stop="dialog2=false">Close</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <br>
                <v-text>Groups:</v-text><br><v-divider></v-divider>
                <v-chip :key="group.name" v-for="group in selectedgroups" close @input="unselectGroup(group.name)">   {{ group.name }}</v-chip>
                <v-menu v-if="groups.length">
                  <v-btn small color="primary" dark slot="activator" fab><v-icon>add</v-icon></v-btn>
                  <!-- TODO: Get all groups this person is admin of -->
                  <v-list>
                    <v-list-tile v-if="!groups.length && !selectedgroups.length" style="color: red;">You are not a group admin!</v-list-tile>
                    <v-list-tile v-else v-for="group in groups" :key="group.name" @click="selectGroup(group.name)">
                      <v-list-tile-title><v-icon style="margin-top: -5px;">add</v-icon>  {{ group.name }}</v-list-tile-title>
                    </v-list-tile>
                  </v-list>
                </v-menu>
              </v-card-text>
            </v-card>

            <v-text-field required style="margin-top: 20px;" v-model="contestname" id="contestname" name="contestname" label="Contest Name"></v-text-field>
            <v-checkbox label="Public" v-model="visible"></v-checkbox>
            <v-btn type="button" large class="light-green accent-3 green--text text--darken-4" style="margin-top: 10px; width: 100%; margin-left: 0px;" to="" @click="postContest()">Create Contest</v-btn>
          </v-flex>

        </v-layout>
      </v-form>

    </v-container>
  </div>
</template>

<script>
// eslint-disable-next-line
import moment from 'vue-moment'
import axios from 'axios';

export default {
  name: 'createcontest',
  components: {

  },
  data () {
    return {
      searchtitle: '',
      searchtags: '',
      contestdate: '',
      dialog2: false,
      contestname: '',
      visible: false,
      detailPopup: false,
      first: 0,
      alertTask: false,
      alertDate: false,
      alertName: false,
      alertAxios: false,
      axiosError: '',
      items: [],
      selectedtags: [],
      tasks: [],
      groups: [ { name: 'Group 1' }, { name: 'Group 2' }, { name: 'Group 3' }, { name: 'Group 4' }, { name: 'Group 5' } ],
      selectedgroups: [],
      empty: [],
      loading: true
    };
  },
  methods: {
    // This method moves task object from items array to tasks array
    addTask(id) {
      var temp = this.items.find(x => x.taskid === id);
      this.items.splice(this.items.indexOf(temp), 1);
      this.tasks.push(temp);
    },
    // This method moves task object from tasks array to items array
    removeTask(id) {
      var temp = this.tasks.find(x => x.taskid === id);
      this.tasks.splice(this.tasks.indexOf(temp), 1);
      this.items.push(temp);
    },
    // Add groups to selection
    selectGroup(name) {
      var temp = this.groups.find(x => x.name === name);
      this.groups.splice(this.groups.indexOf(temp), 1);
      this.selectedgroups.push(temp);
    },
    // Remove groups to selection
    unselectGroup(name) {
      var temp = this.selectedgroups.find(x => x.name === name);
      this.selectedgroups.splice(this.selectedgroups.indexOf(temp), 1);
      this.groups.push(temp);
    },
    removeSelectedTag(item) {
      this.selectedtags.splice(this.selectedtags.indexOf(item), 1);
      this.selectedtags = [...this.selectedtags];
    },
    // This posts data to api
    postContest() {

      // Ensure required fields are filled out
      if(this.tasks.length == 0) {
        this.alertTask = true;
        setTimeout(() => {
          this.alertTask = false;
        }, 10000);
        return false;
      }

      if(this.contestdate == '') {
        this.alertDate = true;
        setTimeout(() => {
          this.alertDate = false;
        }, 10000);
        return false;
      }

      if(this.contestname == '') {
        this.alertName = true;
        setTimeout(() => {
          this.alertName = false;
        }, 10000);
        return false;
      }

      let config = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      };

      // Create AXIOS Post request
      axios.post('/api/contest', {
        'contestname': this.contestname,
        'date_start': new Date().toISOString().substring(0, 19),
        'date_end': this.contestdate,
        'visible': this.visible,
        'usergroups': this.selectedgroups,
        'tasks': this.tasks.map(task => task.taskid),
        'contestadmin': 1
      }, config)
        .then(function (resp) {
          window.location = '/contest/' + resp.data;
        })
        .catch(function (error) {
          this.axiosError = error;
          this.alertAxios = true;
          setTimeout(() => {
            this.alertAxios = false;
          }, 30000);
        });

    }
  },
  computed: {
    // Get current date
    now: function () {
      return new Date().toISOString().substring(0, 10);
    },
    filteredItems() {
      return this.items.filter(item => {
        return item.taskname.toLowerCase().includes(this.searchtitle.toLowerCase()) && this.selectedtags.every(selectedtag => item.tasktags.includes(selectedtag));
      });
    }
  },
  mounted() {
    axios.get('/api/tasks?tags=geometry')
      .then(response => {
        this.items = response.data;
        this.loading = false;
      });
  }
};
</script>

<style scoped>

.vlink {
  cursor: pointer;
}

#taskselection {
  /* margin-left: -10%; */
}

.search {
  width: 45%;
  margin-bottom: -15px;
}
</style>
