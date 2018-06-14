<template>
  <div id="contestdashboard">
    <div v-if="expired" style="margin-top: 20px; font-size: 20pt;">
      This contest is no longer active!
    </div>

    <!-- Layout container -->
    <v-container v-else>
      <!-- Required field alerts -->
      <v-alert
        :value="alertCfHandle"
        type="error"
        transition="scale-transition"
        style="margin-bottom: 10px; width: 90%;"
      >
        Codeforces Handle missing or wrong! Set/Change it in your dashboard.
      </v-alert>

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
                <div slot="header">
                  <b>{{ task.taskid }}:</b> {{ task.taskname }} ({{task.codeforces_id}})
                  <br>
                  <small style="float: left; margin-top: 9px; margin-right: 10px;">
                    Difficulty ({{ task.codeforces_index }}): 
                  </small>
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
                    <v-btn flat color="orange" :href="task.codeforces_url" target="_blank">Solve</v-btn>
                  </v-card-actions>

                </v-card>

              </v-expansion-panel-content>

            </v-expansion-panel>

            <v-data-table v-else :headers="headers" :items="taskanalytics" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td>{{ props.item.user }}</td>
                <td class="text-xs-center" v-for="taskResult in props.item.verdicts" v-bind:key="taskResult">
                  {{ taskResult }}
                </td>
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
                <v-btn color="primary" @click.native="forceUpdate()">Refresh Analytics</v-btn>                
              </div>
            </v-card-title>

          </v-card>
        </v-flex>

      </v-layout>

    </v-container>
  </div>
</template>

<script>
import axios from "axios";
import * as momentjs from "moment";

export default {
  name: "contestdashboard",
  components: {},
  data() {
    return {
      name: "loading...",
      code: "loading...",
      tasks: [],
      date_end: "",
      exists: 1,
      expired: false,
      joined: false,
      admin: true,
      analytics: true,
      taskanalytics: [],
      headers: [
        {
          text: "User",
          value: "user",
          align: "center",
          class: "header-1"
        }
      ],
      alertCfHandle: false,
      users: []
    };
  },
  async created() {
    var contest = {};
    await axios
      .get(`/api/contest?code=${this.$route.params.id}`)
      .then(response => {
        if (response.data === null || typeof response.data === "undefined")
          return;
        contest = response.data;
        this.name = response.data.contestname;
        this.code = response.data.contestcode;
        this.date_end = response.data.date_end;
        this.tasks = Array.isArray(response.data.tasks)
          ? response.data.tasks
          : [response.data.tasks];
        this.tasks.forEach(task => this.headers.push({
          text: `${task.taskid}(${task.codeforces_id+task.codeforces_index})`,
          value: task.taskid,
          align: "center"
        }))
        if (momentjs(new Date()).isSameOrAfter(this.date_end)) {
          this.expired = true;
        }
      })
      .catch(error => {
        this.exists = 0;
        console.log(error);
        window.location = "/404";
      });

    // check if user has already joined the contest
    await axios
      .get(`/api/contests.joined?user=${localStorage.getItem("userid")}`)
      .then(response => {
        if (response.data === null || typeof response.data === "undefined")
          return;
        let res = Array.isArray(response.data) ? response.data : [response.data];
        if (res.some(joinedContest => joinedContest.contest === this.code)) this.joined = true;
      });

    if (contest.contestadmin == localStorage.getItem("userid")) {
      // get all users in contest
      let users = []
      await axios
        .get(
          `/api/contest.joined?code=${contest.contestcode}`
        ).then(response => {
          if (response.data === null || typeof response.data === "undefined")
            return;
          users = (Array.isArray(response.data) ? response.data : [response.data]).map(contestUser => contestUser.user);
        });
      this.users = users;
      users.forEach(async user => {
        await axios
          .get(
            `/api/contest.results?user=${user}&contest=${contest.contestcode}`
          )
          .then(response => {
            if (response.data === null || typeof response.data === "undefined")
              return;

            var row = {
              user: JSON.parse(localStorage.getItem("data")).login,
              verdicts: []
            };
            this.tasks.forEach(task => {
              let filteredTaskAnalytics = response.data.filter(taskData => taskData.task === task.taskid)
              if(filteredTaskAnalytics && filteredTaskAnalytics.length !== 0) {
                row.verdicts.push(filteredTaskAnalytics[0].verdict)
              } else {
                row.verdicts.push("-")
              }
            })
            this.taskanalytics.push(row);
          })
          .catch(err => {
            // catch 400-client error: codeforces handle wrong/missing
            // if (err.response.status === 400) {
            //   this.alertCfHandle = true;
            // } else {
              console.log(err);
            // }
          });
      })
    } 
  },
  methods: {
    // Curtesy of 30-seconds-of-code
    copyToClipboard(str) {
      str = window.location;
      const el = document.createElement("textarea");
      el.value = str;
      el.setAttribute("readonly", "");
      el.style.position = "absolute";
      el.style.left = "-9999px";
      document.body.appendChild(el);
      const selected =
        document.getSelection().rangeCount > 0
          ? document.getSelection().getRangeAt(0)
          : false;
      el.select();
      document.execCommand("copy");
      document.body.removeChild(el);
      if (selected) {
        document.getSelection().removeAllRanges();
        document.getSelection().addRange(selected);
      }
    },

    async joinContest() {
      let config = {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      };
      await axios.post("/api/contests.joined", {
        user: localStorage.getItem("userid"),
        contest: this.code
      }, config)
      .then((res) => this.joined = true);
    },

    async leaveContest() {
      let config = {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      };
      await axios.delete('/api/contests.joined',
        {
          data: {
            'user': localStorage.getItem('userid'),
            'contest': this.code
          },
          config
        }).then((res) => this.joined = false);
    },

    async forceUpdate() {
      this.taskanalytics = []
      this.users.forEach(async user => {
        await axios
          .get(
            `/api/contest.results?user=${user}&contest=${this.code}&force=1`
          )
          .then(response => {
            console.log(response.data)            
            if (response.data === null || typeof response.data === "undefined")
              return;

            var row = {
              user: JSON.parse(localStorage.getItem("data")).login,
              verdicts: []
            };

            this.tasks.forEach(task => {
              let filteredTaskAnalytics = response.data.filter(taskData => taskData.task === task.taskid)
              if(filteredTaskAnalytics && filteredTaskAnalytics.length !== 0) {
                row.verdicts.push(filteredTaskAnalytics[0].verdict)
              } else {
                row.verdicts.push("-")
              }
            })
            this.taskanalytics.push(row);
          })
          .catch(err => {
            // catch 400-client error: codeforces handle wrong/missing
            // if (err.response.status === 400) {
            //   this.alertCfHandle = true;
            // } else {
              console.log(err);
            // }
          });
          console.log(this.taskanalytics)
      });
    }
  },
  computed: {}
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

.header-1 {
  font-style: oblique;
}
</style>
