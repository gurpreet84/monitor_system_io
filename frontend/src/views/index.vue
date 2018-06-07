<style scoped>
    @import '../styles/common.css';
</style>
<template>
    <div class="layout">
        <Sider :style="{position: 'fixed', height: '100vh', left: 0, overflow: 'auto'}">
            <Menu :active-name="current_item.id" theme="dark" width="auto" @on-select="changeArray">
                <MenuItem name="add-array">
                    <Icon type="plus"></Icon>
                    <span>Add Array</span>
                </MenuItem>
                <MenuItem  v-for="(array, index) in arrays"  :name="array.id" :key="index"><Icon type="monitor"></Icon>{{ array.name }}</MenuItem> 
            </Menu>
        </Sider>
        <Layout :style="{marginLeft: '200px'}">
            <Header :style="{background: '#fff', boxShadow: '0 2px 3px 2px rgba(0,0,0,.1)'}"></Header>
            <Content :style="{padding: '0 16px 16px'}">
                <Breadcrumb :style="{margin: '16px 0'}">
                    <BreadcrumbItem>{{ current_item.name }}</BreadcrumbItem>
                </Breadcrumb>
                <Card>
                    <router-view></router-view>
                </Card>
            </Content>
        </Layout>
    </div>
</template>
<script>
    export default {
        data () {
            return {           
            }
        },
        computed:{
            arrays(){
                return this.$store.state.arrays;
            },
            current_item(){
                let item = this.$store.state.current_item;
                item.id = item.id.toString();
                return item;
            }
        },
        created(){
            this.$http.get('/api/array').then((response)=>{
                this.$store.commit('setArray',  response.data);
            }).catch((error)=>{
                this.$Message.error(error);
            });  
        },
        methods: {
            changeArray(id){
                if (id == 'add-array'){
                    this.$router.push({ name: 'array_add'});
                }else{
                    this.$router.push({ name: 'array', params: { array_id: id }});
                }  
            }
        }
    }
</script>
