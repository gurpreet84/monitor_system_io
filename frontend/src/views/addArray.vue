<style scoped>

</style>
<template>
  <div>
    <Form ref="arrayValidate" :model="array" :rules="ruleValidate" :label-width="150">
        <FormItem label="Array Name" prop="name">
            <Input v-model="array.name" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem label="Array mangt IP" prop="ip">
            <Input v-model="array.ip" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem label="Email" prop="email">
            <Input v-model="array.email" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem>
            <Row>
                <Col span="4" offset="10">
                    <Button type="primary" @click="addArray">Add New Array</Button>
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
            },
            ruleValidate:{
                name: [
                    {required: true, message: "The name cannot be empty", trigger: 'blur'}
                ],
                ip: [
                    { required: true, message: "The ip cannot be empty", trigger: 'blur'},
                    { validator(rule, value, callback, source, options) {
                            var errors = [];
                            var re = /^(?:(?:2[0-4]\d|25[0-5]|1\d{2}|[1-9]?\d)\.){3}(?:2[0-4]\d|25[0-5]|1\d{2}|[1-9]?\d)$/;
                            if (!re.test(value)){
                                errors.push("Not IPV4 address");
                            }
                            
                            callback(errors);
                         }, trigger: 'blur'
                    }
                ],
                email:[
                    { required: true, message: 'Mailbox cannot be empty', trigger: 'blur' },
                    { type: 'email', message: 'Incorrect email format', trigger: 'blur'}
                ]
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
            this.$refs['arrayValidate'].validate((valid)=>{
                if(valid){
                    this.$http.post('/api/array/add', this.array).then((response)=>{
                        let array = response.data;
                        this.$store.commit('addArray', array);
                        this.$Message.success('Add success, be patient, background job start to collect iops info');
                    }).catch((error) => {
                        this.$Message.error({
                            content: error,
                            duration: 5});
                    })
                }else{
                    this.$Message.error(
                        {
                            content: "Form validate failed",
                            duration: 5
                        }
                    )
                }
            })
        }
    }
}
</script>



