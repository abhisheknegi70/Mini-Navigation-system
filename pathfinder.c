#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_NODES 50
#define INF INT_MAX

typedef struct {
    int dest;
    int weight;
} Edge;

typedef struct {
    char name[100];
    Edge edges[MAX_NODES];
    int edge_count;
} Node;

Node graph[MAX_NODES];
int node_count = 0;

int dijkstra(int start, int end, int path[]) {
    int dist[MAX_NODES];
    int visited[MAX_NODES];
    int parent[MAX_NODES];
    
    for (int i = 0; i < node_count; i++) {
        dist[i] = INF;
        visited[i] = 0;
        parent[i] = -1;
    }
    
    dist[start] = 0;
    
    for (int count = 0; count < node_count - 1; count++) {
        int min = INF, min_index = -1;
        
        for (int v = 0; v < node_count; v++) {
            if (!visited[v] && dist[v] < min) {
                min = dist[v];
                min_index = v;
            }
        }
        
        if (min_index == -1) break;
        
        visited[min_index] = 1;
        
        for (int i = 0; i < graph[min_index].edge_count; i++) {
            int v = graph[min_index].edges[i].dest;
            int weight = graph[min_index].edges[i].weight;
            
            if (!visited[v] && dist[min_index] != INF && 
                dist[min_index] + weight < dist[v]) {
                dist[v] = dist[min_index] + weight;
                parent[v] = min_index;
            }
        }
    }
    
    if (dist[end] == INF) {
        return -1;
    }
    
    int path_len = 0;
    int current = end;
    while (current != -1) {
        path[path_len++] = current;
        current = parent[current];
    }
    
    for (int i = 0; i < path_len / 2; i++) {
        int temp = path[i];
        path[i] = path[path_len - 1 - i];
        path[path_len - 1 - i] = temp;
    }
    
    return dist[end];
}

int find_node_id(const char* name) {
    for (int i = 0; i < node_count; i++) {
        if (strcmp(graph[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

void load_graph(const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Error opening file: %s\n", filename);
        exit(1);
    }
    
    fscanf(fp, "%d", &node_count);
    
    for (int i = 0; i < node_count; i++) {
        fscanf(fp, "%s", graph[i].name);
        graph[i].edge_count = 0;
    }
    
    int from, to, weight;
    while (fscanf(fp, "%d %d %d", &from, &to, &weight) == 3) {
        graph[from].edges[graph[from].edge_count].dest = to;
        graph[from].edges[graph[from].edge_count].weight = weight;
        graph[from].edge_count++;
        
        graph[to].edges[graph[to].edge_count].dest = from;
        graph[to].edges[graph[to].edge_count].weight = weight;
        graph[to].edge_count++;
    }
    
    fclose(fp);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <graph_file> <start_building> <end_building>\n", argv[0]);
        return 1;
    }
    
    load_graph(argv[1]);
    
    int start = find_node_id(argv[2]);
    int end = find_node_id(argv[3]);
    
    if (start == -1 || end == -1) {
        fprintf(stderr, "Error: Building not found\n");
        return 1;
    }
    
    int path[MAX_NODES];
    int distance = dijkstra(start, end, path);
    
    if (distance == -1) {
        printf("NO_PATH\n");
    } else {
        printf("%d\n", distance);
        int i = 0;
        while (path[i] != end) {
            printf("%s,", graph[path[i]].name);
            i++;
        }
        printf("%s\n", graph[path[i]].name);
    }
    
    return 0;
}
