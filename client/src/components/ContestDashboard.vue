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
            <v-subheader class="display-1" style="margin-top: 2% !important;">Contest {{ name }}
              <v-btn v-if="!joined" color="primary" style="margin-left: 1rem;" @click="joinContest()">Join contest</v-btn>
              <v-btn v-if="joined" color="error" style="margin-left: 1rem;" @click="leaveContest()">Leave contest</v-btn>
            </v-subheader>

            <div>
              <v-subheader style="width: 21.2rem;">Contest code:
                <v-text-field :value="code" disabled style="width: 100px; margin-left: 10px; margin-top: 10px;"></v-text-field>
                <v-tooltip right>
                  <v-icon slot="activator" style="cursor: pointer;" tooltip @click="copyToClipboard()">open_in_new</v-icon>
                  <span>Copy link to clipboard</span>
                </v-tooltip>
              </v-subheader>
            </div>

            <v-expansion-panel popout v-if="!analytics">

             <v-expansion-panel-content v-for="task in tasks" :key="task.taskid">
               <div slot="header">{{ task.taskname }} <br><small style="float: left; margin-top: 9px; margin-right: 10px;">Difficulty ({{ task.codeforces_index }}): </small>
                 <v-progress-linear v-if="task.taskname === 'A'" style="float:left; width: 100px;" value="20" buffer-value="20" color="green"></v-progress-linear>
                 <v-progress-linear v-else-if="task.taskname === 'B'" style="float:left; width: 100px;" value="40" buffer-value="40" color="cyan"></v-progress-linear>
                 <v-progress-linear v-else-if="task.taskname === 'C'" style="float:left; width: 100px;" value="60" buffer-value="60" color="yellow"></v-progress-linear>
                 <v-progress-linear v-else-if="task.taskname === 'D'" style="float:left; width: 100px;" value="80" buffer-value="80" color="orange"></v-progress-linear>
                 <v-progress-linear v-else-if="task.taskname === 'E'" style="float:left; width: 100px;" value="100" color="red"></v-progress-linear>
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

           <v-data-table v-else :headers="headers" :items="desserts" hide-actions class="elevation-1">
             <template slot="items" slot-scope="props">
               <td>{{ props.item.name }}</td>
               <td class="text-xs-right">{{ props.item.calories }}</td>
               <td class="text-xs-right">{{ props.item.fat }}</td>
               <td class="text-xs-right">{{ props.item.carbs }}</td>
               <td class="text-xs-right">{{ props.item.protein }}</td>
               <td class="text-xs-right">{{ props.item.iron }}</td>
             </template>
           </v-data-table>

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

          <v-card v-if="admin" class="analytics" style="margin-top: 10%;">

            <v-card-title primary-title>
              <div  style="width: 100% !important">
                <h3 class="headline mb-0">Track Progress</h3>
                <v-divider></v-divider>
                <v-btn color="primary" @click.native="analytics=!analytics">Analytics</v-btn>
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
      name: 'loading...',
      code: 'loading...',
      tasks: [],
      date_end: '',
      exists: 1,
      expired: false,
      joined: false,
      admin: true,
      analytics: true,
      taskanalytics: [],
      headers: [],
      desserts: []
    };
  },
  async created() {
    var contest = {};
    await axios.get('/api/contest?code=' + this.$route.params.id)
      .then((response) => {
        contest = response.data;
        this.name = response.data.contestname;
        this.code = response.data.contestcode;
        this.date_end = response.data.date_end;
        this.tasks = Array.isArray(response.data.tasks) ? response.data.tasks : [response.data.tasks];
        if(momentjs(new Date()).isSameOrAfter(this.date_end)) {
          this.expired = true;
        }
      })
      .catch((error) => {
        this.exists = 0;
        console.log(error);
        window.location = '/404';
      });

    await axios.get('/api/contest.joined?user=' + localStorage.getItem('userid'))
      .then((response) => {
        if(response.data.includes(contest))
          this.joined = true;
      });

    var temp = [{
      'text':'User', 'value':'user'
    },
    {
      'text': "Hid", 'value': 'hello'
    }];

    // for(var i = 0; i < 1; i++) {
    //   temp.push({ text: "Hid", value: 'hello' });
    // }

    this.headers = temp;

    if(contest.contestadmin == localStorage.getItem('userid')) {
      axios.get('/api/contest.results?user=' + localStorage.getItem('userid') + '&contest=' + contest.contestcode)
      .then((response) => {
        var row = {
          value: false,
          user: JSON.parse(localStorage.getItem('data')).login,
        }

        for(var x = 0; x < response.data.length; x++) {
          row[response.data[x].task] = response.data[x].verdict;
        }

        this.taskanalytics.push(row)
        console.log(row);
      });
    }

    this.taskanalytics = [{
      'user': 'Qo2770',
      '1': 'Hi'
    }]

  },
  methods: {
    // Curtesy of 30-seconds-of-code
    copyToClipboard(str) {
      str = window.location;
      const el = document.createElement('textarea');
      el.value = str;
      el.setAttribute('readonly', '');
      el.style.position = 'absolute';
      el.style.left = '-9999px';
      document.body.appendChild(el);
      const selected =
        document.getSelection().rangeCount > 0 ? document.getSelection().getRangeAt(0) : false;
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      if (selected) {
        document.getSelection().removeAllRanges();
        document.getSelection().addRange(selected);
      }
    },

    joinContest() {
      axios.post('/api/contest.joined',
        {
          'user': localStorage.getItem('userid'),
          'contest': this.code
        });

      this.joined = true;
    },

    leaveContest() {
      // TODO: Implement leaving when endpoint is made
      // axios.post('/api/contest.joined',
      //   {
      //     'user': localStorage.getItem('userid'),
      //     'contest': this.code
      //   });

      this.joined = false;
    }
  },
  computed: {

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
