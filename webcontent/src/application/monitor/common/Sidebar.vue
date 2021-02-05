<template>
    <div class="sidebar-monitor">
        <el-menu
                class="sidebar-el-menu"
                :default-active="onRoutes"
                :collapse="collapse"
                text-color="rgb(239 239 241)"
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
                    application: 'monitor',
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
            this.getData();
            this.getPermArr()
        },
        methods: {
            // 获取导航栏信息
            getData() {
                let username = localStorage.getItem('username');
                this.$http.get(`sys/api/user/role/?username=${username}&application=${this.query.application}&type=menu`, {
                    headers: {
                        'token':localStorage.getItem('token')
                    }
                }).then((res) => {
                    if(res.data.length!=0 || res.data!=null){
                        this.items = treeDataTranslate(res.data, 'id');
                    }
                }).catch(function (error) {
                    console.log("失败==" + error);
                    alert(error);
                });
            },
            // 获取角色按钮权限
            getPermArr() {
                let username = localStorage.getItem('username');
                this.$http.get(`sys/api/user/role/?username=${username}&application=${this.query.application}&type=button`, {
                    headers: {
                        'token':localStorage.getItem('token')
                    }
                }).then((res) => {
                    if(res.data.length!=0 || res.data!=null){
                        let btnPermissionArr = res.data;
                        localStorage.setItem('btnPermission', JSON.stringify(btnPermissionArr));
                    }
                }).catch(function (error) {
                    console.log("失败==" + error);
                    alert(error);
                });
            }
        }
    };
</script>

<style lang="scss" scoped>
    .sidebar-monitor {
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom: 0;
        overflow-y: scroll;
        background: #898bad;
    }
    .sidebar-el-menu{
        background: #494b79;
    }
     .el-menu-item i,.el-submenu__title i{
         color: #d9dbe0;
    }
    .sidebar-monitor::-webkit-scrollbar {
        width: 0;
    }

    .sidebar-el-menu:not(.el-menu--collapse) {
        width: 250px;
    }

    .sidebar-monitor > ul {
        height: 100%;
    }

    /deep/ .el-menu-item:hover{
        background-color: #727496;
        color:#fff!important;
    }
    /deep/ el-menu-item:focus{
        background-color: #727496;
        color:#fff
    }
    /deep/ .el-submenu__title:hover{
        background-color: #727496;
        color:#fff!important;
    }
    /deep/ .el-submenu__title:focus{
        background-color: #727496;
        color:#fff
    }

    /deep/ .el-menu--collapse {
        width: 67px;
    }
    .el-menu-item:hover i,.el-submenu__title:hover i{
        color: #fff;
    }
    /deep/ .el-menu{
        background-color: #494b79!important;
    }
    /deep/ .el-menu-item:focus, .el-menu-item:hover{
        background-color: #727496;
        color:#fff!important;
    }
    /deep/ .el-menu-item.is-active{
        color: #fff!important;
    }
    /deep/ .el-menu--popup{
        background-color: #494b79!important;
		padding: 0!important;
    }
	/deep/ .el-menu{
		background-color: #494b79!important;
	}
</style>
<style>
    /* .el-menu{
        background-color: #494b79;
    } */
    .el-menu-item:focus,.el-menu-item:hover{
        background-color: #727496;
        color:#fff!important;
    }
	.el-menu--popup{
		background-color: #494b79!important;
		padding:0!important;
	}
    .el-menu-item.is-active{
        color: #fff!important;
    }
</style>
