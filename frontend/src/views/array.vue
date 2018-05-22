<style scoped>
    .headstyle {
        text-align: center;
    }
    .array-info {
        font-weight: bold;
        font-size: 20px;
    }
</style>
<template>
   <div class="headstyle">
       <h1>{{ array.name }}</h1>
       <Row>
           <Col span="12">
            <div class="array-info">
                IP: <span>{{ array.ip}}</span>
            </div>
           </Col>
           <Col span=12>
           <div class="array-info">
                Email: <span>{{ array.email }}</span>
           </div>
           </Col>
        </Row>
        <Table border :columns="columns" :data="table_data"></Table>
   </div>
</template>
<script>
export default {
   data(){
       return {
            array:{},
            columns: [{
                title: 'Name',
                key: 'name',
                render: (h, params) =>{
                    let name = params.row.name;
                    return h('router-link', {
                            attrs:{
                                to: '/array/container/' + params.row.id
                            }
                        }, name)
                }
            },
            {
                title: 'description',
                key: 'description'
            }],
            table_data: [],
       }
   },
   created(){
       this.array = this.$store.state.arrays[this.$route.params.array_id];
       if(!this.array){
           this.array = JSON.parse(window.localStorage.getItem('current_item'));
       }else{
           window.localStorage.setItem('current_item', JSON.stringify(this.array));
       }
       this.$store.commit('setItem', this.array);
       this.fetchData(this.$route.params.array_id);
   },
   watch: {
       '$route' (to, from){
          this.array = this.$store.state.arrays[to.params.array_id];
          this.$store.commit('setItem', this.array); 
          window.localStorage.setItem('current_item', JSON.stringify(this.array));
          this.fetchData(to.params.array_id);
       }
   },
   methods: {
       fetchData(id){
          this.$http.get('/api/array/' + id + '/container').then(response => {
              this.table_data = response.data;
          }).catch(err=>{
              this.$Message.error(err);
          })
       }
   }
}
</script>
