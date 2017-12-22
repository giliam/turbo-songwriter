<template>
    <tr class="item content">
        <td>
            <router-link :to="{name: 'song_detail', params:{item_id: item.id}}" tag="a" class="header">{{item.title}}</router-link>
        </td>
        <td>
            <template v-if="item.author">
                {{item.author.firstname}} {{item.author.lastname}}
            </template>
        </td>
        <td>
            <template v-if="item.editor">
                {{item.editor.name}}
            </template>
        </td>
        <td>
            {{item.page_number}}/{{item.old_page_number}}
        </td>
        <td>
            <template v-if="item.latex_code">
                {{ t('Has a latex code') }}
            </template>
            <template v-else>
                {{ t('Has no code') }}
            </template>
        </td>
    </tr>
</template>

<script>
    export default {
        name: "Songinfos",
        props:{
            item: Object
        },
        methods:{
        }
    }
</script>