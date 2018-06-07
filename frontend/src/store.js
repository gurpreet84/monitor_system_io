import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);
const store = new Vuex.Store({
    state: {
        arrays: [],
        arrayObjects: {},
        current_item:{
            name: 'Add Array',
            id: 'add-array'
        }
    },
    mutations: {
        setArray(state, arrs){
            state.arrays = arrs;
            for(let arr of arrs){
                state.arrayObjects[arr.id] = arr;
            }
        },
        addArray(state, arr){
            state.arrays.push(arr);
            state.arrayObjects[arr.id] = arr;
        },
        setItem(state, item){
            state.current_item = item;
        }
    }
});

export default store;
