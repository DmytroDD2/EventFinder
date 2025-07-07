import api from "@/api/api";
import { useMutation } from "@tanstack/react-query";
import { useQueryClient } from "@tanstack/react-query";

const patchUserRole = async (userId: string) => {
    const params = new URLSearchParams();
    params.append('user_id', userId.toString());
    return (await api.patch('/users/role', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
        },
    })).data;
};

export const usePatchUserRole = () => {
    const queryClient = useQueryClient();
    const rechargeMutation = useMutation({
        mutationFn: (userId: string) => patchUserRole(userId),
        onSuccess: (_data, userId) => {
            queryClient.invalidateQueries({ queryKey: ["profile", userId] });
        },
    });

    return {
        patchUserRole: rechargeMutation.mutateAsync,
        isPatching: rechargeMutation.isPending,
        patchError: rechargeMutation.error,
        isPatchSuccess: rechargeMutation.isSuccess,
    };
};
