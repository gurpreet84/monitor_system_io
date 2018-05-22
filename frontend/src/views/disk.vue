<style scoped>

</style>
<template>
 <div>
   <DatePicker v-model="daterange" 
               type="datetimerange" 
               placeholder="Select date and time" 
               style="width: 300px"
               @on-ok="handleOK"></DatePicker>
   <ve-line :data="chartData" :settings="chartSettings"></ve-line>
</div>
</template>
<script>
import moment from 'moment';
export default {
  data(){
      return {
          chartData: {},
          chartSettings:{},
          daterange: []
      }
  },
  created(){
      this.getIOPS(this.$route.params.disk_id);
  },
  methods: {
      getIOPS(id){
          this.$http.get('/api/iops/array/disk/' + id).then(resp => {
              if(resp.data.length === 0){
                  this.$Message.info({
                      content: 'No IOPS info',
                      duration: 5
                  })
              }else{
                  this.fillChart(resp.data);
              }
          });
      },
      fillChart(data){
          let rows = [];
          let disknames = Object.keys(data[0]['iops']);
          for(let order of data){
              let iopses = { time: moment.unix(order.timestamp).format("MM-DD HH:mm") };
              for(let diskname in order.iops){
                  iopses[diskname] = order.iops[diskname];
              }
              rows.push(iopses);
          }
          let disknames_1 = disknames.slice();
          disknames_1.push('time');
          this.chartData = {
              columns: disknames_1,
              rows: rows
          }
          this.chartSettings = {
              metrics: disknames,
              dimension: ['time']
          }
      },
      handleOK(){
          let start = this.daterange[0].getTime() / 1000;
          let end = this.daterange[1].getTime() / 1000;

          this.$http.get('/api/iops/array/disk/' + this.$route.params.disk_id,
                        {
                            params: {
                                start: start,
                                end: end
                            }
                        }).then(resp => {
              if(resp.data.length === 0){
                  this.$Message.info({
                      content: 'No IOPS info',
                      duration: 5
                  })
              }else{
                  this.fillChart(resp.data);
              }
          });
      }
  }
}
</script>
