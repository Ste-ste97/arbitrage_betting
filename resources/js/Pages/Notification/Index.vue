<template>
    <div class="surface-card shadow-2 border-round p-4">
        <div class="text-xl text-900 font-medium mb-5">Inbox</div>
        <div class="flex justify-content-between pb-3">
            <Button class="p-button-outlined p-button-primary w-6 mr-2" label="Mark All As Read" @click="markAllRead()"></Button>
            <Button class="p-button-outlined p-button-danger w-6 mr-2" label="Clear All" @click="deleteAll()"></Button>
        </div>
        <ul class="list-none p-0 m-0">
            <Link v-for="notification in notifications.data" :href="route('notifications.show', notification.id)">
                <li class="lg:px-3 lg:py-2 align-items-center hover:text-900 hover:surface-100 border-round cursor-pointer pb-3 border-bottom-1 surface-border">
                    <div class="font-medium text-900 mb-2 pt-2">{{ notification.data.title }}</div>
                    <div class="line-height-3 text-600" style="max-width: 30rem">{{ notification.data.message }}</div>
                    <Badge v-if="!notification.read_at" value="New"></Badge>
                </li>
            </Link>
        </ul>
        <p v-if="notifications.total === 0">Nothing to show</p>
        <Paginator :first="firstItem" :rows="notifications.per_page" :totalRecords="notifications['total']"
                   @page="changePage($event)"
        ></Paginator>
    </div>
</template>

<script>
import AuthenticatedLayout from "@/Layouts/Authenticated.vue";
import {Head} from "@inertiajs/vue3";
import {Link} from '@inertiajs/vue3'

export default {
    layout     : AuthenticatedLayout,
    components : {
        AuthenticatedLayout,
        Head,
        Link
    },
    props      : {
        notifications : Object,
    },
    methods    : {
        changePage(data) {
            this.$inertia.get(
                route('notifications.index'),
                {page : data.page + 1},
                {
                    preserveScroll : true,
                    preserveState  : true,
                }
            );
        },
        markAllRead() {
            this.$confirm.require({
                message : 'Are you sure you want to mark everything as read?',
                header  : 'Confirmation',
                icon    : 'pi pi-exclamation-triangle',
                accept  : () => {
                    this.$inertia.post(route('notifications.markAllRead'));
                },
                reject  : () => {
                }
            });
        },
        deleteAll() {
            this.$confirm.require({
                message : 'Are you sure you want to delete everything?',
                header  : 'Confirmation',
                icon    : 'pi pi-exclamation-triangle',
                accept  : () => {
                    this.$inertia.post(route('notifications.massDestroy'));
                },
                reject  : () => {
                }
            });
        }
    },
    computed   : {
        firstItem() {
            return (this.notifications.current_page - 1) * this.notifications.per_page
        }
    },
};
</script>
