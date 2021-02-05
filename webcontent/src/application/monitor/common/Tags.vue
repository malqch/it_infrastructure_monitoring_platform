<template>
    <div class="tags-monitor" v-if="showTags">
        <ul>
            <li class="tags-li-monitor" v-for="(item,index) in tagsList" :class="{'active': isActive(item.path)}" :key="index">
                <router-link :to="item.path" class="tags-li-monitor-title">
                    {{item.title}}
                </router-link>
                <span class="tags-li-icon" @click="closeTags(index)"><i class="el-icon-close"></i></span>
            </li>
        </ul>
        <div class="tags-close-box-monitor">
            <el-dropdown @command="handleTags">
                <el-button size="mini" type="primary">
                    标签选项<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu size="small" slot="dropdown">
                    <el-dropdown-item command="other">关闭其他</el-dropdown-item>
                    <el-dropdown-item command="all">关闭所有</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </div>
</template>

<script>
    import bus from './bus';
    export default {
        data() {
            return {
                tagsList: []
            }
        },
        methods: {
            isActive(path) {
                return path === this.$route.fullPath;
            },
            // 关闭单个标签
            closeTags(index) {
                const delItem = this.tagsList.splice(index, 1)[0];
                const item = this.tagsList[index] ? this.tagsList[index] : this.tagsList[index - 1];
                if (item) {
                    delItem.path === this.$route.fullPath && this.$router.push(item.path);
                }else{
                    this.$router.push('/');
                }
            },
            // 关闭全部标签
            closeAll(){
                this.tagsList = [];
                this.$router.push('/');
            },
            // 关闭其他标签
            closeOther(){
                const curItem = this.tagsList.filter(item => {
                    return item.path === this.$route.fullPath;
                })
                this.tagsList = curItem;
            },
            // 设置标签
            setTags(route){
                const isExist = this.tagsList.some(item => {
                    return item.path === route.fullPath;
                })
                if(!isExist){
                    if(this.tagsList.length >= 8){
                        this.tagsList.shift();
                    }
                    this.tagsList.push({
                        title: route.meta.title,
                        path: route.fullPath,
                        name: route.matched[0].components.default.name
                    })
                }
                bus.$emit('tags', this.tagsList);
            },
            handleTags(command){
                command === 'other' ? this.closeOther() : this.closeAll();
            }
        },
        computed: {
            showTags() {
                return this.tagsList.length > 0;
            }
        },
        watch:{
            $route(newValue){
                this.setTags(newValue);
            }
        },
        created(){
           this.setTags(this.$route);
            // 监听关闭当前页面的标签页
            bus.$on('close_current_tags', () => {
                for (let i = 0, len = this.tagsList.length; i < len; i++) {
                    const item = this.tagsList[i];
                    if(item.path === this.$route.fullPath){
                        if(i < len - 1){
                            this.$router.push(this.tagsList[i+1].path);
                        }else if(i > 0){
                            this.$router.push(this.tagsList[i-1].path);
                        }else{
                            this.$router.push('/');
                        }
                        this.tagsList.splice(i, 1);
                        break;
                    }
                }
            })
        }
    }

</script>


<style lang="scss" scoped>
    .tags-monitor {
        position: relative;
        height: 30px;
        overflow: hidden;
        background: #272c4b;
        padding-right: 120px;
        box-shadow: 0 5px 10px #373855;
    }

    .tags ul {
        box-sizing: border-box;
        width: 100%;
        height: 100%;
    }

    .tags-li-monitor {
        float: left;
        margin: 3px 5px 2px 3px;
        border-radius: 3px;
        font-size: 12px;
        overflow: hidden;
        cursor: pointer;
        height: 23px;
        line-height: 23px;
        border: 1px solid #3c4163;
        background: #24273e;
        padding: 0 5px 0 12px;
        vertical-align: middle;
        color: #fff;
        -webkit-transition: all .3s ease-in;
        -moz-transition: all .3s ease-in;
        transition: all .3s ease-in;
    }

    .tags-li-monitor:not(.active):hover {
        background: #2c3661;
    }

    .tags-li-monitor.active {
        color: #fff;
        background: #82a7f3;
    }

    .tags-li-monitor-title {
        float: left;
        max-width: 80px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        margin-right: 5px;
        color: #fff;
    }

    .tags-li-monitor.active .tags-li-monitor-title {
        color: #fff;
    }

    .tags-close-box-monitor {
        position: absolute;
        right: 0;
        top: 0;
        box-sizing: border-box;
        padding-top: 1px;
        text-align: center;
        width: 110px;
        height: 30px;
        background: #272c4b;
        box-shadow: -3px 0 15px 3px rgba(0, 0, 0, .1);
        z-index: 10;
    }
    .el-dropdown-menu,.el-dropdown-menu__item--divided:before{
        background-color: #656896;
    }
    .el-dropdown-menu{
        border: 1px solid #656896;
    }

   .el-dropdown-menu__item{
        color: #c5c7cb
    }
    .el-dropdown-menu__item:hover{
        background-color: #727496;
        color: #fff
    }
    .el-popper[x-placement^=bottom] .popper__arrow,.el-popper[x-placement^=bottom]  .popper__arrow:after{
                border-bottom-color:#656896!important;
            }
</style>
