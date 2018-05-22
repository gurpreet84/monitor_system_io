import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);
const store = new Vuex.Store({
    state: {
        arrays: {},
        current_item:{
            name: 'Add Array',
            id: 'add-array'
        }
    },
    mutations: {
        setArray(state, arrs){
            let arrays = {};
            for(let arr of arrs){
                arrays[arr.id] = arr;
            }
            state.arrays = arrays;
        },
        addArray(state, arr){
            state.arrays[arr.id] = arr;
        },
        setItem(state, item){
            state.current_item = item;
        }
    }
});

export default store;
