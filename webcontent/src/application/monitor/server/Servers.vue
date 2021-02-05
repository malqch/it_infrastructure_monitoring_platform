<template>
    <el-row>
        <el-col :span="4">
            <el-card :body-style="{ padding: '2px' }">
<!--                <img src="../../assets/img/3.jpeg" class="image">-->
                <div style="padding: 14px;">
                    <span>物理服务器</span>
                    <div class="bottom clearfix">
                        <a href="http://localhost:8070/#/monitor/physical_server">进入</a>
                    </div>
                </div>
            </el-card>
        </el-col>

        <el-col :span="4" >
            <el-card :body-style="{ padding: '2px' }">
<!--                <img src="../../assets/img/2.jpeg" class="image">-->
                <div style="padding: 14px;">
                    <span>虚拟服务器</span>
                    <div class="bottom clearfix">
                        <a href="http://localhost:8070/#/monitor/virtual_server">进入</a>
                    </div>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>
<style>
    .time {
        font-size: 13px;
        color: #999;
    }

    .bottom {
        margin-top: 13px;
        line-height: 12px;
    }

    .button {
        padding: 0;
        float: right;
    }

    .image {
        width: 100%;
        display: block;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }

    .clearfix:after {
        clear: both
    }
</style>

<script>
    export default {
        data() {
            return {
                currentDate: new Date()
            };
        }
    }
</script>