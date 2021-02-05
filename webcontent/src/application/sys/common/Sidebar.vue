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
                <template v-if="item.subs">
                    <el-submenu :index="item.id" :key="item.id">
                        <template slot="title">
                            <i :class="item.icon"></i>
                            <span slot="title">{{ item.name }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu
                                v-if="subItem.subs"
                                :index="subItem.menu_url"
                                :key="subItem.id"
                            >
                                <template slot="title">{{ subItem.name }}</template>
                                <el-menu-item
                                    v-for="(threeItem,i) in subItem.subs"
                                    :key="i"
                                    :index="threeItem.menu_url"
                                >{{ threeItem.name }}</el-menu-item>
                            </el-submenu>
                            <el-menu-item
                                v-else
                                :index="subItem.menu_url"
                                :key="subItem.id"
                            >{{ subItem.name }}</el-menu-item>
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
                application: 'sys',
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
        this.getPermArr();
    },
    methods: {
        getData() {
            this.$http.get(`sys/api/user/role/?username=${this.username}&application=${this.query.application}&type=menu`, {
                headers: {
                    'token': this.token,
                }
            }).then((res) => {
                this.items = res.data;
            }).catch(function (error) {
                console.log("失败==" + error);
            });
        },
        // 获取角色按钮权限
        getPermArr() {
            this.$http.get(`sys/api/user/role/?username=${this.username}&application=${this.query.application}&type=button`, {
                headers: {
                    'token': this.token,
                }
            }).then((res) => {
                let btnPermissionArr = res.data;
                localStorage.setItem('btnPermission', JSON.stringify(btnPermissionArr));
            }).catch(function (error) {
                console.log("失败==" + error);
                // alert(error);
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