<style scoped>

</style>
<template>
<div>
    <DatePicker v-model="daterange" 
               type="datetimerange" 
               placeholder="Select date and time" 
               style="width: 300px"
               @on-ok="handleOK"></DatePicker>
   <ve-line :data="chartData" :settings="chartSettings" :theme="theme"></ve-line>
   <Table border :columns="columns" :data="table_data"></Table>
</div>
</template>
<script>
import moment from 'moment';
export default {
  data(){
      return {
          theme:{
              line: {
                  smooth: false
              }
          },
          chartData: {},
          chartSettings:{},
          daterange:[],
          columns: [
              {
                  title: 'Name',
                  key: 'name',
                  render: (h, params) =>{
                    return h('router-link', {
                            attrs:{
                                to: '/array/container/disk/' + params.row.id
                            }
                        }, params.row.name)
                }
              },
              {
                  title: 'Size(GB)',
                  key: 'size'
              },
              {
                  title: 'IsInUse',
                  key: 'isInUse'
              }
          ],
          table_data: []
      }
  },
  created(){
      this.getDiskInfo(this.$route.params.container_id);
      this.getIOPS(this.$route.params.container_id);
  },
  methods: {
      getDiskInfo(id){
          this.$http.get('/api/array/container/' + id + '/disk').then(response => {
              this.table_data = response.data;
          });
      },
      getIOPS(id){
          this.$http.get('/api/iops/array/container/' + id).then(response => {
              if(response.data.length === 0){
                  this.$Message.info({
                      content: 'No IOPS info',
                      duration: 5
                  })
              }else{
                  this.fillChart(response.data);
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
          this.chartSettings = {
              metrics: disknames,
              dimension: ['time']
          }
          let disknames_1 = disknames.slice();
          disknames_1.push('time');
          this.chartData = {
              columns: disknames_1,
              rows: rows
          }  
      },
      handleOK(){
          let start = this.daterange[0].getTime() / 1000;
          let end = this.daterange[1].getTime() / 1000;

          this.$http.get('/api/iops/array/container/' + this.$route.params.dape_id,
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
