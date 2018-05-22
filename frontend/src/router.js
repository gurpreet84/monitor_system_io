
const routers = [
    {
        path: '/',
        name: 'index',
        meta: {
            title: 'Index'
        },
        redirect: '/array/add',
        component: (resolve) => require(['./views/index.vue'], resolve),
        children: [
            {
                path: 'array/add',
                title: 'Add Array',
                name: 'array_add',
                component: resolve => require(['./views/addArray.vue'], resolve)

            },
            {
                path: 'array/:array_id',
                title: 'Array',
                name: 'array',
                component: resolve => require(['./views/array.vue'], resolve)
            },
            {
                path: 'array/container/:container_id',
                title: 'Container',
                name: 'container',
                component: resolve => require(['./views/container.vue'], resolve)
            },
            {
                path: 'array/container/disk/:disk_id',
                title: 'Disk',
                name: 'disk',
                component: resolve => require(['./views/disk.vue'], resolve)
            }
        ]
    }
];
export default routers;