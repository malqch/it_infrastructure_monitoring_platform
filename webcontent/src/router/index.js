import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

export default new Router({
    routes: [
        { path: '/', redirect: '/index' },
        { path: '/index', component: () => import('../components/page/Index.vue'), meta: { title: '首页' } },
        {
            path: '/asset',
            redirect: '/asset/dashboard',
            component: () => import('../application/asset/common/Home.vue'),
            meta: { title: '登录' },
            children: [
                {
                    path: '/asset/dashboard',
                    component: () => import('../application/asset/Dashboard.vue'),
                    meta: { title: '首页' }
                },
                {
                    path: '/asset/tag',
                    component: () => import('../application/asset/tag/Tag.vue'),
                    meta: { title: 'Tag' }
                },
                {
                    path: '/asset/disk',
                    component: () => import('../application/asset/parts/Disk.vue'),
                    meta: { title: 'DISK' }
                },
                { path: '/asset/hba', component: () => import('../application/asset/parts/Hba.vue'), meta: { title: 'HBA卡' } },
                { path: '/asset/hca', component: () => import('../application/asset/parts/Hca.vue'), meta: { title: 'HCA卡' } },
                { path: '/asset/nic', component: () => import('../application/asset/parts/Nic.vue'), meta: { title: 'NIC卡' } },
                { path: '/asset/ssd', component: () => import('../application/asset/parts/Ssd.vue'), meta: { title: 'SSD卡' } },
                { path: '/asset/datacenter', component: () => import('../application/asset/datacenter/DataCenter.vue'), meta: { title: '数据中心' }},
                { path: '/asset/room', component: () => import('../application/asset/datacenter/Room.vue'), meta: { title: '机房' }},
                { path: '/asset/rack', component: () => import('../application/asset/datacenter/Rack.vue'), meta: { title: '机柜' }},
                { path: '/asset/server', component: () => import('../application/asset/device/Server'), meta: { title: '服务器'}},
                { path: '/asset/virtualserver', component: () => import('../application/asset/device/VirtualServer'), meta: { title: '虚拟服务器'}},
                { path: '/asset/storage', component: () => import('../application/asset/device/Storage'), meta: { title: '存储'}},
                { path: '/asset/staff', component: () => import('../application/asset/logic_resourse/Staff'), meta: { title: '人员管理'}},
                { path: '/asset/business', component: () => import('../application/asset/logic_resourse/Business'), meta: { title: '业务'}},
                { path: '/asset/contract', component: () => import('../application/asset/logic_resourse/Contract'), meta: { title: '文档管理'}},
                { path: '/asset/vendor', component: () => import('../application/asset/logic_resourse/Vendor'), meta: { title: '供应商'}},
                { path: '/asset/network', component: () => import('../application/asset/device/Network.vue'), meta: { title: '网络设备'}}
            ]
        },
        {
            path: '/sys',
            redirect: '/sys/dashboard',
            component: () => import('../application/sys/common/Home.vue'),
            meta: { title: '登录' },
            children: [
                {
                    path: '/sys/dashboard',
                    component: () => import('../application/sys/Dashboard2.vue'),
                    meta: { title: '系统首页' }
                },
                { path: '/sys/user', component: () => import('../application/sys/User.vue'), meta: { title: '用户管理' } },
                { path: '/sys/role', component: () => import('../application/sys/Role.vue'), meta: { title: '角色管理' } },
                { path: '/sys/menu', component: () => import('../application/sys/Menu.vue'), meta: { title: '菜单管理' } },
                { path: '/sys/password', component: () => import('../application/sys/Password.vue'), meta: { title: '修改密码' } }
            ]
        },
        {
            path: '/monitor',
            redirect: '/monitor/dashboard',
            component: () => import('../application/monitor/common/Home.vue'),
            meta: { title: '登录' },
            children: [
                { path: '/monitor/dashboard', component: () => import('../application/monitor/Dashboard2.vue'), meta: { title: '系统首页' }},
                { path: '/monitor/databases', component: () => import('../application/monitor/database/Databases.vue'), meta: { title: '数据库管理' } },
                // { path: '/monitor/db_item', component: () => import('../application/monitor/database/DBItem.vue'), meta: { title: '数据库监控项' } },
                { path: '/monitor/dm_db_visualize', component: () => import('../application/monitor/database/DMDatabasesVisualization'), meta: { title: '可视化达梦数据库监控' } },
                { path: '/monitor/oracle_visualize', component: () => import('../application/monitor/database/OracleVisualize.vue'), meta: { title: 'oracle监控' } },
                { path: '/monitor/mysql_visualize', component: () => import('../application/monitor/database/MysqlVisualize.vue'), meta: { title: 'mysql监控' } },

                { path: '/monitor/middleware', component: () => import('../application/monitor/middleware/Middleware.vue'), meta: { title: '中间件管理' } },
                // { path: '/monitor/middleware_item', component: () => import('../application/monitor/middleware/MiddlewareItem.vue'), meta: { title: '中间件监控项' } },
                { path: '/monitor/middleware/monitor', component: () => import('../application/monitor/middleware/MiddlewareMonitor.vue'), meta: { title: 'redis监控' } },
                { path: '/monitor/middleware/websphere', component: () => import('../application/monitor/middleware/WebsphereMiddleware.vue'), meta: { title: 'websphere监控' } },
                { path: '/monitor/middleware/weblogic', component: () => import('../application/monitor/middleware/WeblogicMiddleware'), meta: { title: 'weblogic监控' } },
                { path: '/monitor/middleware/rabbitmq', component: () => import('../application/monitor/middleware/RabbitmqMonitor.vue'), meta: { title: 'rabbitmq监控' } },
                // { path: '/monitor/servers', component: () => import('../application/monitor/server/Servers.vue'), meta: {title: '服务器管理'}},
                { path: '/monitor/physical_server', component: () => import('../application/monitor/server/PhysicalServer.vue'), meta: {title: '物理服务器'}},
                { path: '/monitor/virtual_server', component: () => import('../application/monitor/server/VirtualServer.vue'), meta: {title: '虚拟服务器'}},
                // { path: '/monitor/server_monitor', component: () => import('../application/monitor/server/ServerMonitor.vue'), meta: {title: '服务器监控项'}},
                { path: '/monitor/monitor_visualize', component: () => import('../application/monitor/server/MonitorVisualization'), meta: {title: '可视化服务器监控'}},

                { path: '/monitor/storage_display', component: () => import('../application/monitor/storage/StorageDisplay.vue'), meta: { title: '存储管理'}},
                { path: '/monitor/storage_item', component: () => import('../application/monitor/storage/StorageItem.vue'), meta: { title: '存储监控项' } },
                //{ path: '/monitor/storage_visualize', component: () => import('../application/monitor/storage/StorageVisualization.vue'), meta: { title: '可视化存储监控' } },
				{ path: '/monitor/storage_visualize', component: () => import('../application/monitor/storage/StorageHW.vue'), meta: { title: '存储监控' } },
				{ path: '/monitor/storageh3', component: () => import('../application/monitor/storage/StorageH3.vue'), meta: { title: '华三存储监控' } },

                { path: '/monitor/router', component: () => import('../application/monitor/network_equipment/Router.vue'), meta: {title: '路由器'}},
                { path: '/monitor/firewall', component: () => import('../application/monitor/network_equipment/Firewall.vue'), meta: {title: '防火墙'}},
                { path: '/monitor/load_balance', component: () => import('../application/monitor/network_equipment/LoadBalance.vue'), meta: {title: '负载均衡'}},
                { path: '/monitor/switch', component: () => import('../application/monitor/network_equipment/Switch.vue'), meta: {title: '交换机'}},
                // { path: '/monitor/network_monitor', component: () => import('../application/monitor/network_equipment/NetworkMonitor.vue'), meta: {title: '网络设备监控项管理'}},
                { path: '/monitor/network_visualize', component: () => import('../application/monitor/network_equipment/NetworkVisualize.vue'), meta: {title: '交换机监控'}},
                // { path: '/monitor/fireWall_visualize', component: () => import('../application/monitor/network_equipment/FirewallVisualize.vue'), meta: {title: '防火墙监控'}},
				{ path: '/monitor/h3cfireWall_visualize', component: () => import('../application/monitor/network_equipment/H3CFirewallVisualize.vue'), meta: {title: '防火墙监控'}},
				{ path: '/monitor/h3cload_balance', component: () => import('../application/monitor/network_equipment/H3CLoadBalance.vue'), meta: {title: '负载均衡监控'}},

                { path: '/monitor/alarm_severity', component: () => import('../application/monitor/alarm/AlarmSeverity.vue'), meta: {title: '告警等级管理'}},
                { path: '/monitor/alarm_strategy', component: () => import('../application/monitor/alarm/AlarmStrategy.vue'), meta: {title: '告警策略管理'}},
                { path: '/monitor/alarm_rule', component: () => import('../application/monitor/alarm/AlarmRule.vue'), meta: {title: '告警规则管理'}},
                { path: '/monitor/alarm_detail', component: () => import('../application/monitor/alarm/AlarmDetail.vue'), meta: {title: '告警详情'}},
                { path: '/monitor/level_alarm_count', component: () => import('../application/monitor/alarm/LevelCountAlarm.vue'), meta: {title: '不同等级告警数量统计'}},
                { path: '/monitor/type_alarm_count', component: () => import('../application/monitor/alarm/ServerTypeCountAlarm.vue'), meta: {title: '不同类型告警数量统计'}},

                { path: '/monitor/snmp_monitor_config', component: () => import('../application/monitor/network_equipment/NetworkMonitor.vue'), meta: {title: '网络设备监控项管理'}},
                { path: '/monitor/other_monitor_config', component: () => import('../application/monitor/server/ServerMonitor.vue'), meta: {title: '其他监控项'}},
            ]
        },
        {
            path: '/automation',
            redirect: '/automation/dashboard',
            component: () => import('../application/automation/common/Home.vue'),
            meta: { title: '登录' },
            children: [
                { path: '/automation/dashboard', component: () => import('../application/automation/Dashboard.vue'), meta: { title: '系统首页' }},
                { path: '/automation/scripts', component: () => import('../application/automation/script/Scripts.vue'), meta: { title: '脚本管理' } },
                { path: '/automation/script_execution', component: () => import('../application/automation/script/ScriptExecute.vue'), meta: { title: '脚本执行' } },
                { path: '/automation/script_timing_execution', component: () => import('../application/automation/script/ScriptTimingExecute'), meta: { title: '定时任务' } },
                { path: '/automation/script_log', component: () => import('../application/automation/script/ScriptLog.vue'), meta: { title: '脚本执行日志' } },

                { path: '/automation/pxeserver', component: () => import('../application/automation/install/PxeServer.vue'), meta: { title: 'pxe管理' } },
                { path: '/automation/jobcheck', component: () => import('../application/automation/install/JobCheck.vue'), meta: { title: '端口检查' } },
                { path: '/automation/jobchecklog', component: () => import('../application/automation/install/JobCheckLog.vue'), meta: { title: '端口检查日志' } },
                { path: '/automation/jobinstall', component: () => import('../application/automation/install/JobInstall.vue'), meta: { title: '物理机装机' } },
                { path: '/automation/jobinstalllog', component: () => import('../application/automation/install/JobInstallLog.vue'), meta: { title: '装机日志' } },

                { path: '/automation/vms', component: () => import('../application/automation/huaweiyun/Vms.vue'), meta: { title: '虚拟机管理' } },
                { path: '/automation/template', component: () => import('../application/automation/huaweiyun/Template.vue'), meta: { title: '虚拟机模板' } },
                { path: '/automation/network', component: () => import('../application/automation/huaweiyun/Network.vue'), meta: { title: '网络' } },
                { path: '/automation/security_group', component: () => import('../application/automation/huaweiyun/SecurityGroup.vue'), meta: { title: '安全组' } },
                { path: '/automation/huaweiyun', component: () => import('../application/automation/huaweiyun/Huaweiyun.vue'), meta: { title: '华为云环境管理' } },

                { path: '/automation/lungroup', component: () => import('../application/automation/storage/LunGroup.vue'), meta: { title: 'LUN'}},
                { path: '/automation/host', component: () => import('../application/automation/storage/Host.vue'), meta: {title: 'HOST'}},
                { path: '/automation/mapview', component: () => import('../application/automation/storage/MapView.vue'), meta: { title: '映射视图'}},

                {path: '/automation/patrol', component: () => import('../application/automation/patrol/patrol.vue'), meta: {title: '巡检任务'}},
                { path: '/automation/patrol_execution', component: () => import('../application/automation/patrol/patrolExecute.vue'), meta: { title: '巡检执行' } },
                { path: '/automation/patrol_log', component: () => import('../application/automation/patrol/patrolLog.vue'), meta: { title: '巡检执行日志' } },
            ]
        },
        {
            path: '/login',
            component: () => import('../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {

            path: '*',
            redirect: '/404'
        },
        { path: '/404', component: () => import('../components/page/404.vue'), meta: { title: '404' } },
        { path: '/403', component: () => import('../components/page/403.vue'), meta: { title: '403' } }
    ]
});
