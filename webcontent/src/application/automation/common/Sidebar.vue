<template>
    <div class="sidebar">
        <el-menu
                class="sidebar-el-menu"
                :default-active="onRoutes"
                :collapse="collapse"
                background-color="#324157"
                text-color="#bfcbd9"
                active-text-color="#20a0ff"
                unique-opened
                router
        >
            <template v-for="item in items">
                <template v-if="item.children">
                    <el-submenu :index="JSON.stringify(item.id)" :key="item.id">
                        <template slot="title">
                            <i :class="item.icon"></i>
                            <span slot="title">{{ item.name }}</span>
                        </template>
                        <template v-for="subItem in item.children">
                            <el-submenu
                                    v-if="subItem.children"
                                    :index="subItem.menu_url"
                                    :key="subItem.id"
                            >
                                <template slot="title">{{ subItem.name }}</template>
                                <el-menu-item
                                        v-for="(threeItem,i) in subItem.children"
                                        :key="i"
                                        :index="threeItem.menu_url"
                                >{{ threeItem.name }}
                                </el-menu-item>
                            </el-submenu>
                            <el-menu-item
                                    v-else
                                    :index="subItem.menu_url"
                                    :key="subItem.id"
                            >{{ subItem.name }}
                            </el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.menu_url" :key="item.index">
                        <i :class="item.icon"></i>
                        <span slot="title">{{ item.name }}</span>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script>
    import bus from './bus';
    import {treeDataTranslate} from '../../../util/formatData'
    export default {
        data() {
            return {
                collapse: false,
                items: [],
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10,
                    application: 'automation',
                },
            };
        },
    computed: {
        onRoutes() {
            return this.$route.path.replace('/', '');
        }
    },
    created() {
        // 通过 Event Bus 进行组件间通信，来折叠侧边栏
        bus.$on('collapse', msg => {
            this.collapse = msg;
            bus.$emit('collapse-content', msg);
        });
        this.token =  localStorage.getItem('token');
        this.username = localStorage.getItem('username');
        this.getData();
        this.getPermArr()
    },
    methods: {
        // 获取导航栏信息
        getData() {
            this.$http.get(`sys/api/user/role/?username=${this.username}&application=${this.query.application}&type=menu`, {
                headers: {
                    'token': this.token
                }
            }).then((res) => {
                this.items = treeDataTranslate(res.data, 'id');
            }).catch( (error)=> {
                console.log("失败==" + error);
                this.$message.error(JSON.stringify(error.response.data));
            });
        },
        // 获取角色按钮权限
        getPermArr() {
            this.$http.get(`sys/api/user/role/?username=${this.username}&application=${this.query.application}&type=button`, {
                headers: {
                    'token': this.token
                }
            }).then((res) => {
                let btnPermissionArr = res.data;
                localStorage.setItem('btnPermission', JSON.stringify(btnPermissionArr));
            }).catch( (error)=> {
                console.log("失败==" + error);
                this.$message.error(JSON.stringify(error.response.data));
            });
        }
    }
};
</script>

<style scoped>
    .sidebar {
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom: 0;
        overflow-y: scroll;
    }

    .sidebar::-webkit-scrollbar {
        width: 0;
    }

    .sidebar-el-menu:not(.el-menu--collapse) {
        width: 250px;
    }

    .sidebar > ul {
        height: 100%;
    }
	/deep/ .el-menu--popup{
		padding: 0!important;
	}
</style>
<style>
	.el-menu--popup{
		padding: 0!important;
	}
</style>