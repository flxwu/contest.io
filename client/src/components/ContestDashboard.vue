<template>
  <div id="contestdashboard">
    <!-- Layout container -->
    <v-container>

      <v-layout>

        <v-flex xs6>
            <!-- Task LIst -->
            <v-subheader class="display-1" style="margin-top: 2% !important;">Contest {{ $route.params.id }}</v-subheader>

            <router-link tag="v-avatar" to="/profile/1" class="grey lighten-4 avatar vlink" size="35px">
              <img src="https://vuetifyjs.com/static/doc-images/lists/1.jpg" alt="avatar">
              <div><v-subheader style="width: 200px;">Herr Hörner</v-subheader></div>
            </router-link>
            <v-expansion-panel popout>

             <v-expansion-panel-content v-for="item in items" :key="item.taskid">

               <div slot="header">{{ item.taskname }} <br><small style="float: left; margin-top: 9px; margin-right: 10px;">Difficulty: </small>
                   <v-progress-linear v-if="item.codeforces_index === 'A'" style="float:left; width: 100px;" value="25" buffer-value="25" color="green"></v-progress-linear>
                   <v-progress-linear v-if="item.codeforces_index === 'B'" style="float:left; width: 100px;" value="50" buffer-value="50" color="yellow"></v-progress-linear>
                   <v-progress-linear v-if="item.codeforces_index === 'C'" style="float:left; width: 100px;" value="75" buffer-value="75" color="orange"></v-progress-linear>
                   <v-progress-linear v-if="item.codeforces_index === 'D'" style="float:left; width: 100px;" value="100" color="red"></v-progress-linear>
               </div>

              <v-card>

                <!-- <v-card-text>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</v-card-text> -->

                <!-- Tags -->
                <div class="chiptag">
                  <v-chip small :key="tag"  v-for="tag in item.tasktags">{{ tag }}</v-chip>
                </div>

                <!-- TODO: add link to codeforces -->
                <v-card-actions>
                  <v-btn flat color="orange" :href="item.codeforces_url">Solve</v-btn>
                </v-card-actions>

              </v-card>

             </v-expansion-panel-content>

           </v-expansion-panel>

        </v-flex>

        <v-flex xs2>
        </v-flex>

        <v-flex xs4>
          <v-card class="cardprogress">

            <v-card-title primary-title>
              <div  style="width: 100% !important">
                <h3 class="headline mb-0">Progress</h3>
                <v-divider></v-divider>
                <div>0 / {{ items.length }} Tasks completed (<span>{{ (0 / items.length) * 100 }}%</span>)</div>
                <div>Time remaining: 5 days, 11 hours</div>
              </div>
            </v-card-title>

          </v-card>
        </v-flex>

      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'contestdashboard',
  components: {

  },
  data () {
    return {
      items: [

      ]
    }
  },
  mounted() {
    axios.get("http://localhost:5000/api/tasks?tags=geometry")
      .then(response => {  this.items = response.data })
  }
}
</script>

<style scoped>
.cardprogress {
  margin-top: 30% !important;
}

.avatar {
  margin-left: -52% !important;
  margin-bottom: 2%;
  margin-top: 1%;
}

.chiptag {
  margin-left: 10px;
}

.vlink {
  cursor: pointer;
}
</style>
