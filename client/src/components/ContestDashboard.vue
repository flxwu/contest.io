<template>
  <div id="contestdashboard">
    <div v-if="expired" style="margin-top: 20px; font-size: 20pt;">
      This contest is no longer active!
    </div>

    <!-- Layout container -->
    <v-container v-else>

      <v-layout>

        <v-flex xs6>

            <!-- Task List -->
            <v-subheader class="display-1" style="margin-top: 2% !important;">Contest {{ name }}</v-subheader>

            <div><v-subheader style="width: 270px;">Contest code: <v-text-field :value="code" disabled style="width: 100px; margin-left: 10px; margin-top: 10px;"></v-text-field></v-subheader> </div>
            <v-expansion-panel popout>

             <v-expansion-panel-content v-for="task in tasks" :key="task.taskid">
               <div slot="header">{{ task.taskname }} <br><small style="float: left; margin-top: 9px; margin-right: 10px;">Difficulty ({{ task.codeforces_index }}): </small>
                   <v-progress-linear v-if="task.codeforces_index.split('')[0] === 'A'" style="float:left; width: 100px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                   <v-progress-linear v-else-if="task.codeforces_index.split('')[0] === 'B'" style="float:left; width: 100px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                   <v-progress-linear v-else-if="task.codeforces_index.split('')[0] === 'C'" style="float:left; width: 100px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                   <v-progress-linear v-else-if="task.codeforces_index.split('')[0] === 'D'" style="float:left; width: 100px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                   <v-progress-linear v-else-if="task.codeforces_index.split('')[0] === 'E'" style="float:left; width: 100px;" value="100" color="red"></v-progress-linear>
                   <v-progress-linear v-else style="float:left; width: 100px;" value="100" color="red"></v-progress-linear>
               </div>

              <v-card>

                <!-- Tags -->
                <div class="chiptag">
                  <v-chip small :key="tag"  v-for="tag in JSON.parse(task.tasktags)">{{ tag }}</v-chip>
                </div>

                <v-card-actions>
                  <v-btn flat color="orange" :href="task.codeforces_url">Solve</v-btn>
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
                <div>0 / {{ tasks.length }} Tasks completed (<span>{{ (0 / tasks.length) * 100 }}%</span>)</div>
                <div>Time remaining: {{ date_end | moment("from", true) }}</div>
              </div>
            </v-card-title>

          </v-card>
        </v-flex>

      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios';
import * as momentjs from 'moment';

export default {
  name: 'contestdashboard',
  components: {},
  data() {
    return {
      items: [],
      name: '',
      code: '',
      tasks: [],
      date_end: null,
      exists: 1,
      expired: false
    };
  },
  mounted() {
    axios.get('/api/contest?code=' + this.$route.params.id)
      .then(response => {
        console.log(response.data);
        this.name = response.data.contestname;
        this.code = response.data.contestcode;
        this.date_end = response.data.date_end;
        this.tasks = [response.data.tasks];
        if(momentjs(new Date()).isSameOrAfter(this.date_end)) {
          this.expired = true;
        }
      })
      .catch(() => {
        this.exists = 0;
        //window.location = '/404';
      });
  }
};
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
