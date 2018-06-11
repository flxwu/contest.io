<template>
  <div>
    <p class="">{{ user.login }}</p>
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
          console.log(typeof(this.user));
        }
      });
  }
};
</script>

<style scoped>

</style>
