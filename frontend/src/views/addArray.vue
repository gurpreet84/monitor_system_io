<style scoped>

</style>
<template>
  <div>
    <Form :model="array" :label-width="150">
        <FormItem label="Array Name">
            <Input v-model="array.name" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem label="Array mangt IP">
            <Input v-model="array.ip" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem label="Email">
            <Input v-model="array.email" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem>
            <Row>
                <Col span="4" offset="10">
                    <Button type="primary" @click="addArray">ADD</Button>
                </Col>
            </Row>
        </FormItem>
    </Form>
</div>
</template>
<script>
export default {
    data (){
        return {
            array: {
                name: '',
                ip:'',
                email: '',
            }
        }
    },
    created(){
        let item = {
            name: 'Add Array',
            id: 'add-array'
        };
        this.$store.commit('setItem', item);
        window.localStorage.setItem('current_item', JSON.stringify(item));
   },
    methods: {
        addArray: function(){
            this.$http.post('/api/array/add', this.array).then((response)=>{
                let array = response.data;
                this.$store.commit('addArray', array);
                this.$Message.success('Add success, be patient, background job start to collect iops info');
            }).catch((error) => {
                this.$Message.error(error);
            })
        }
    }
}
</script>



